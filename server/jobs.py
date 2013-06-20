#!/usr/bin/env python
import redis
import json
import argparse
import pprint
import mturk_vision
import base64
import uuid
import pickle
from hadoop_parse import scrape_hadoop_jobs


class UnauthorizedException(Exception):
    """User is not authorized to make this call"""


class NotFoundException(Exception):
    """Task was not found"""


class Jobs(object):

    def __init__(self, host, port, db, annotation_redis_host, annotation_redis_port):
        self.args = (host, port, db, annotation_redis_host, annotation_redis_port)
        self.redis_host = host
        self.redis_port = port
        self.db = redis.StrictRedis(host=host, port=port, db=db)
        self.annotation_cache = {}
        self._owner_prefix = 'owner:'
        self._task_prefix = 'task:'
        self._lock_prefix = 'lock:'
        self.annotation_redis_host = annotation_redis_host
        self.annotation_redis_port = annotation_redis_port
        self.hadoop_completed_jobs_cache = set()

    def __reduce__(self):
        return (Jobs, self.args)

    def add_task(self, type, owner, params, secret_params):
        task = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
        data = {'owner': owner, '_params': json.dumps(secret_params),
                'params': json.dumps(params), 'type': type}
        if not self.db.set(self._lock_prefix + task, '', nx=True):
            raise UnauthorizedException
        # TODO: Do these atomically
        self.db.hmset(self._task_prefix + task, data)
        self.db.sadd(self._owner_prefix + owner, task)
        return task

    def _check_owner(self, task, owner):
        if self.db.hget(self._task_prefix + task, 'owner') != owner:
            raise UnauthorizedException

    def _get_task_type(self, task):
        out = self.db.hgetall(self._task_prefix + task)
        out = self.db.hget(self._task_prefix + task, 'type')
        if out is None:
            raise NotFoundException
        return out

    def _check_type(self, task, type):
        if self._get_task_type(task) != type:
            raise NotFoundException

    def _exists(self, task):
        if not self.db.exists(self._lock_prefix + task):
            raise NotFoundException

    def get_task(self, task, owner):
        self._exists(task)
        self._check_owner(task, owner)
        out = self.db.hgetall(self._task_prefix + task)
        out = {k: v for k, v in out.items() if not k.startswith('_')}
        return out

    def get_task_secret(self, task, owner):
        self._exists(task)
        self._check_owner(task, owner)
        return json.loads(self.db.hget(self._task_prefix + task, '_params'))

    def delete_task(self, task, owner):
        self._exists(task)
        self._check_owner(task, owner)
        task_type = self._get_task_type(task)
        if task_type == 'annotation':
            manager = self.get_annotation_manager(task)
        # TODO: Do these atomically
        self.db.delete(self._task_prefix + task, self._lock_prefix + task)
        self.db.srem(self._owner_prefix + owner, task)
        if task_type == 'annotation':
            manager.destroy()  # TODO: MTurk specific
            try:
                del self.annotation_cache[task]
            except KeyError:
                pass
        # TODO: For Hadoop jobs kill the task if it is running
        # TODO: For worker/crawl/model jobs kill the worker process or send it a signal

    def update_job(self, row, columns):
        self.db.hmset(self._task_prefix + row, columns)

    def update_hadoop_jobs(self, hadoop_jobtracker):
        for row, columns in scrape_hadoop_jobs(hadoop_jobtracker, self.hadoop_completed_jobs_cache).items():
            # NOTE: We do this at this point as a job may not exist but is finished completed/failed in hadoop
            if columns.get('status', '') in ('completed', 'failed'):
                self.hadoop_completed_jobs_cache.add(row)
            try:
                self._exists(row)
                self._check_type(row, 'process')
            except NotFoundException:
                continue
            # TODO: Need to do this atomically with the exists check
            self.update_job(row, columns)

    def get_tasks(self, owner):
        outs = {}
        for job_key in self.db.smembers(self._owner_prefix + owner):
            # TODO: Error check if something gets removed while we are accumulating
            task = self._task_prefix + job_key
            if self.db.hget(task, 'owner') == owner:
                out = self.db.hgetall(task)
                out = {k: v for k, v in out.items() if not k.startswith('_')}
                outs[task.split(':', 1)[1]] = out
        return outs

    def get_annotation_manager(self, task, sync=False):
        self._exists(task)
        self._check_type(task, 'annotation')
        try:
            return self.annotation_cache[task]
        except KeyError:
            data = self.db.hgetall(self._task_prefix + task)
            p = json.loads(data['params'])
            ps = json.loads(data['_params'])
            p['sync'] = sync
            p['secret'] = str(ps['secret'])
            p['redis_address'] = self.annotation_redis_host
            p['redis_port'] = int(self.annotation_redis_port)
            p['task_key'] = task
            self.annotation_cache[task] = mturk_vision.manager(data=str(ps['data']), **p)
            return self.annotation_cache[task]

    def get_annotation_manager_check(self, task, owner):
        self._exists(task)
        self._check_type(task, 'annotation')
        self._check_owner(task, owner)
        return self.get_annotation_manager(task)

    def add_work(self, front, queue, **kw):
        push = self.db.lpush if front else self.db.rpush
        push('queue:' + queue, pickle.dumps(kw, -1))

    def get_work(self, queues, timeout=0):
        out = self.db.brpop(['queue:' + x for x in queues], timeout=timeout)
        if not out:
            return
        queue = out[0][:len('queue:')]
        print('Processing job from [%s]' % queue)
        return queue, pickle.loads(out[1])


def main():

    def _get_all_tasks(jobs):
        outs = []
        for job_key in jobs.db.keys('task:*'):
            out = jobs.db.hgetall(job_key)
            outs.append(out)
        return outs

    def _info(args, jobs):
        pprint.pprint(_get_all_tasks(jobs))

    def _destroy(args, jobs):
        jobs.db.flushall()

    def job_worker(db, func, method_args, method_kwargs):
        getattr(db, func)(*method_args, **method_kwargs)

    def _work(args, jobs):
        import inotifyx
        fd = inotifyx.init()
        # NOTE: .git/logs/HEAD is the last thing updated after a git pull/merge
        inotifyx.add_watch(fd, '../.git/logs/HEAD', inotifyx.IN_MODIFY)
        inotifyx.add_watch(fd, '.reloader', inotifyx.IN_MODIFY | inotifyx.IN_ATTRIB)
        while 1:
            work = jobs.get_work(args.queues, timeout=5)
            if work:
                job_worker(**work[1])
            if inotifyx.get_events(fd, 0):
                print('Shutting down due to new update')
                break

    parser = argparse.ArgumentParser(description='Picarus job operations')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=3)
    parser.add_argument('--annotations_redis_host', help='Annotations Host', default='localhost')
    parser.add_argument('--annotations_redis_port', type=int, help='Annotations Port', default=6380)
    subparsers = parser.add_subparsers(help='Commands')

    subparser = subparsers.add_parser('info', help='Display info about jobs')
    subparser.set_defaults(func=_info)

    subparser = subparsers.add_parser('destroy', help='Delete everything in the jobs DB')
    subparser.set_defaults(func=_destroy)

    subparser = subparsers.add_parser('work', help='Do background work')
    parser.add_argument('queues', nargs='+', help='Queues to do work on')
    subparser.set_defaults(func=_work)

    args = parser.parse_args()
    jobs = Jobs(args.redis_host, args.redis_port, 3,
                args.annotations_redis_host, args.annotations_redis_port)
    args.func(args, jobs)

if __name__ == '__main__':
    main()
