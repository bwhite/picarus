import redis
import json
import argparse
import pprint
import mturk_vision


class UnauthorizedException(Exception):
    """User is not authorized to make this call"""


class CapacityException(Exception):
    """Not enough backend REDIS servers"""


class Annotators(object):

    def __init__(self, host, port, db):
        self.db = redis.StrictRedis(host=host, port=port, db=db)
        self.annotator_prefix = 'annot:'  # [task]
        self.available_servers = 'srvr:available'  # [host:port]
        self.cache = {}

    def add_task(self, task, owner, secret, data, params):
        # TODO: Pipeline so that we can be sure modifications are atomic
        # TODO: Check quota here
        # TODO: Move create manager here, as we have it for get manager
        data = {'task': task, 'owner': owner, '_secret': secret, '_data': data,
                'params': json.dumps(params)}
        redis_host_port = self.db.spop(self.available_servers)
        if redis_host_port is None:
            raise CapacityException
        data['_redis_host_port'] = redis_host_port
        # TODO: Ensure that the task doesn't exist
        self.db.hmset(self.annotator_prefix + task, data)
        return redis_host_port

    def get_task(self, task, owner):
        if self.db.hget(self.annotator_prefix + task, 'owner') != owner:
            raise UnauthorizedException
        out = self.db.hgetall(self.annotator_prefix + task)
        out = {k: v for k, v in out.items() if not k.startswith('_')}
        return out

    def get_manager(self, task):
        # TODO: Need to ensure no races due to a worker running while the DB is destroyed
        #       can fix by putting a unique key in state_db, that is verified each call
        #       but needs to lock the race down (check and set?)
        data = self.db.hgetall(self.annotator_prefix + task)
        p = json.loads(data['params'])
        p['setup'] = False
        p['reset'] = False
        p['secret'] = data['_secret']
        redis_host, redis_port = data['_redis_host_port'].split(':')
        p['redis_address'] = redis_host
        p['redis_port'] = int(redis_port)
        # This ensures that the task still exists before we reuse the cache
        try:
            return self.cache[task]
        except KeyError:
            self.cache[task] = mturk_vision.manager(data=data['_data'], **p)
            return self.cache[task]

    def get_task_secret(self, task, owner):
        if self.db.hget(self.annotator_prefix + task, 'owner') != owner:
            raise UnauthorizedException
        return self.db.hget(self.annotator_prefix + task, '_secret')

    def delete_task(self, task, owner):
        if self.db.hget(self.annotator_prefix + task, 'owner') != owner:
            raise UnauthorizedException
        redis_host_port = self.db.hget(self.annotator_prefix + task, '_redis_host_port')
        # TODO: Pipeline
        # TODO: Login to the redis server and flush it
        # TODO: Communicate with remote server to shut it down
        self.db.delete(self.annotator_prefix + task)
        self.db.sadd(self.available_servers, redis_host_port)

    def get_tasks(self, owner):
        outs = {}
        for annot_key in self.db.keys(self.annotator_prefix + '*'):
            # TODO: Error check if something gets removed while we are accumulating
            if self.db.hget(annot_key, 'owner') == owner:
                out = self.db.hgetall(annot_key)
                out = {k: v for k, v in out.items() if not k.startswith('_')}
                outs[annot_key.split(':', 1)[1]] = out
        return outs


def main():

    def _get_all_tasks(annotators):
        outs = []
        for annot_key in annotators.db.keys(annotators.annotator_prefix + '*'):
            out = annotators.db.hgetall(annot_key)
            outs.append(out)
        return outs

    def _flush(args, annotators):
        for annot_key in annotators.db.keys(annotators.annotator_prefix + '*'):
            task = annot_key.split(':', 1)[1]
            print(task)
            annotators.delete_task(task, annotators.db.hget(annot_key, 'owner'))

    def _add_host_port(args, annotators):
        annotators.db.sadd(annotators.available_servers, args.host_port)

    def _delete_host_port(args, annotators):
        annotators.db.srem(annotators.available_servers, args.host_port)

    def _info(args, annotators):
        pprint.pprint(annotators.db.smembers(annotators.available_servers))
        pprint.pprint(_get_all_tasks(annotators))

    parser = argparse.ArgumentParser(description='Picarus annotator operations')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6380)
    parser.add_argument('--redis_db', type=int, help='Redis DB', default=2)
    subparsers = parser.add_subparsers(help='Commands')

    subparser = subparsers.add_parser('add_host_port', help='Add redis host_port to pool')
    subparser.add_argument('host_port', help='host:port')
    subparser.set_defaults(func=_add_host_port)

    subparser = subparsers.add_parser('delete_host_port', help='Delete redis host_port to pool')
    subparser.add_argument('host_port', help='host:port')
    subparser.set_defaults(func=_delete_host_port)

    subparser = subparsers.add_parser('info', help='Display info about annotators')
    subparser.set_defaults(func=_info)

    subparser = subparsers.add_parser('flush', help='Delete all annotators, put their DBs back in the pool')
    subparser.set_defaults(func=_flush)

    args = parser.parse_args()
    users = Annotators(args.redis_host, args.redis_port, args.redis_db)
    args.func(args, users)

if __name__ == '__main__':
    main()
