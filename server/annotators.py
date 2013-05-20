import redis
import json
import argparse
import pprint
import mturk_vision


class UnauthorizedException(Exception):
    """User is not authorized to make this call"""


class NotFoundException(Exception):
    """Task was not found"""


class Annotators(object):

    def __init__(self, host, port):
        self.redis_host = host
        self.redis_port = port
        self.db = redis.StrictRedis(host=host, port=port, db=5)
        self.cache = {}

    def add_task(self, task, owner, secret, data, params):
        data = {'owner': owner, '_secret': secret, '_data': data,
                'params': json.dumps(params)}
        if not self.db.set(task + ':lock', '', nx=True):
            raise UnauthorizedException
        self.db.hmset(task + ':annot', data)
        return self.redis_host, self.redis_port

    def get_task(self, task, owner):
        self.exists(task)
        if self.db.hget(task + ':annot', 'owner') != owner:
            raise UnauthorizedException
        out = self.db.hgetall(task + ':annot')
        out = {k: v for k, v in out.items() if not k.startswith('_')}
        return out

    def exists(self, task):
        if not self.db.exists(task + ':lock'):
            raise NotFoundException

    def get_manager(self, task):
        self.exists(task)
        try:
            return self.cache[task]
        except KeyError:
            data = self.db.hgetall(task + ':annot')
            p = json.loads(data['params'])
            p['sync'] = False
            p['secret'] = data['_secret']
            p['redis_address'] = self.redis_host
            p['redis_port'] = int(self.redis_port)
            self.cache[task] = mturk_vision.manager(data=data['_data'], **p)
            return self.cache[task]

    def get_manager_check(self, task, owner):
        self.exists(task)
        if self.db.hget(task + ':annot', 'owner') != owner:
            raise UnauthorizedException
        return self.get_manager(task)

    def get_task_secret(self, task, owner):
        self.exists(task)
        if self.db.hget(task + ':annot', 'owner') != owner:
            raise UnauthorizedException
        return self.db.hget(task + ':annot', '_secret')

    def delete_task(self, task, owner):
        self.exists(task)
        if self.db.hget(task + ':annot', 'owner') != owner:
            raise UnauthorizedException
        manager = self.get_manager(task)
        self.db.delete(task + ':annot', task + ':lock')
        manager.destroy()
        try:
            del self.cache[task]
        except KeyError:
            pass

    def get_tasks(self, owner):
        outs = {}
        for annot_key in self.db.keys('*:annot'):
            # TODO: Error check if something gets removed while we are accumulating
            if self.db.hget(annot_key, 'owner') == owner:
                out = self.db.hgetall(annot_key)
                out = {k: v for k, v in out.items() if not k.startswith('_')}
                outs[annot_key.split(':', 1)[0]] = out
        return outs


def main():

    def _get_all_tasks(annotators):
        outs = []
        for annot_key in annotators.db.keys('*:annot'):
            out = annotators.db.hgetall(annot_key)
            outs.append(out)
        return outs

    def _info(args, annotators):
        pprint.pprint(_get_all_tasks(annotators))

    def _destroy(args, annotators):
        annotators.db.flushall()

    parser = argparse.ArgumentParser(description='Picarus annotator operations')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6380)
    subparsers = parser.add_subparsers(help='Commands')

    subparser = subparsers.add_parser('info', help='Display info about annotators')
    subparser.set_defaults(func=_info)

    subparser = subparsers.add_parser('destroy', help='Delete everything in the annotation DB')
    subparser.set_defaults(func=_destroy)

    args = parser.parse_args()
    users = Annotators(args.redis_host, args.redis_port)
    args.func(args, users)

if __name__ == '__main__':
    main()
