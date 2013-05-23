#!/usr/bin/env python
import redis
import json
import argparse
import pprint
import mturk_vision


class UnauthorizedException(Exception):
    """User is not authorized to make this call"""


class NotFoundException(Exception):
    """Task was not found"""


class Jobs(object):

    def __init__(self, host, port, db):
        self.redis_host = host
        self.redis_port = port
        self.db = redis.StrictRedis(host=host, port=port, db=db)
        self.annotation_cache = {}
        self._owner_prefix = 'owner:'
        self._task_prefix = 'task:'
        self._lock_prefix = 'lock:'

    def add_task(self, task, type, owner, params, secret_params):
        data = {'owner': owner, '_params': json.dumps(secret_params),
                'params': json.dumps(params), 'type': type}
        if not self.db.set(self._lock_prefix + task, '', nx=True):
            raise UnauthorizedException
        # TODO: Do these atomically
        self.db.hmset(self._task_prefix + task, data)
        self.db.sadd(self._owner_prefix + owner, task)
        return self.redis_host, self.redis_port

    def _check_owner(self, task, owner):
        if self.db.hget(self._task_prefix + task, 'owner') != owner:
            raise UnauthorizedException

    def _get_task_type(self, task):
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
        if self._get_task_type(task) == 'annotation':
            manager = self.get_annotation_manager(task)
        # TODO: Do these atomically
        self.db.delete(self._task_prefix + task, self._lock_prefix + task)
        self.db.srem(self._owner_prefix + owner, task)
        if self._get_task_type(task) == 'annotation':
            manager.destroy()  # TODO: MTurk specific
            try:
                del self.annotation_cache[task]
            except KeyError:
                pass

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

    def get_annotation_manager(self, task):
        self._exists(task)
        self._check_type(task, 'annotation')
        try:
            return self.annotation_cache[task]
        except KeyError:
            data = self.db.hgetall(self._task_prefix + task)
            p = json.loads(data['params'])
            ps = json.loads(data['_params'])
            p['sync'] = False
            p['secret'] = str(ps['secret'])
            p['redis_address'] = self.redis_host
            p['redis_port'] = int(self.redis_port)
            self.annotation_cache[task] = mturk_vision.manager(data=str(ps['data']), **p)
            return self.annotation_cache[task]

    def get_annotation_manager_check(self, task, owner):
        self._exists(task)
        self._check_type(task, 'annotation')
        self._check_owner(task, owner)
        return self.get_annotation_manager(task)


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

    parser = argparse.ArgumentParser(description='Picarus job operations')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=3)
    subparsers = parser.add_subparsers(help='Commands')

    subparser = subparsers.add_parser('info', help='Display info about jobs')
    subparser.set_defaults(func=_info)

    subparser = subparsers.add_parser('destroy', help='Delete everything in the jobs DB')
    subparser.set_defaults(func=_destroy)

    args = parser.parse_args()
    jobs = Jobs(args.redis_host, args.redis_port)
    args.func(args, jobs)

if __name__ == '__main__':
    main()
