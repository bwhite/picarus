import bottle
import hashlib
import os
import base64
import contextlib
import time
import redis
import argparse
import json


def email_auth_factory(email_auth_fn='email_auth.js'):
    EMAIL = json.load(open(email_auth_fn))  # keys as key, secret, admin, url, name
    import boto

    def email_func(email, api_key, login_key=None):
        conn = boto.connect_ses(EMAIL['key'], EMAIL['secret'])
        if login_key is None:
            body = '<h2>Email</h2><pre>%s</pre><h2><h2>API Key (Expires in 24 hours)</h2><pre>%s</pre>' % (email, api_key)
            subject = '[%s] - API Key' % EMAIL['name']
        else:
            body = '<h2>Email</h2><pre>%s</pre><h2>Login Key</h2><pre>%s</pre><h2>API Key (Expires in 24 hours)</h2><pre>%s</pre>' % (email, login_key, api_key)
            subject = '[%s] - Login/API Key' % EMAIL['name']
        return conn.send_email(source=EMAIL['admin'], subject=subject,
                               body=body, to_addresses=email, format='html')
    return email_func


class UnknownUser(Exception):
    """User not in the database"""


class User(object):
    """Picarus User Class

    Public Methods: Safe to use from frontend
    Private Methods: Should not be used in frontend
    """

    def __init__(self, user_db, email, setup=False):
        self._user_db = user_db
        self.email = email
        self.upload_row_prefix = 'userupload%s:' % base64.b64encode(hashlib.sha1(email).digest())[:-1]
        self._stat_keys = ('start', 'finish', 'total_time')
        self._user_prefix = 'user:'
        self._stat_prefix = 'stat:'
        self._api_key_prefix = 'auth:'
        self._login_key_prefix = 'login:'
        self._image_row_prefix = 'image_prefix:'
        self._enabled_col = 'enabled'
        self.key_length = 15
        assert self.key_length % 3 == 0
        assert self.key_length > 0
        if setup:
            self.enable()
        if not self._exists():
            raise UnknownUser

    def _exists(self):
        return self._user_db.exists(self._user_prefix + self.email) == 1

    def enabled(self):
        out = self.hget(self._user_prefix + self.email, self._enabled_col)
        if out is None or int(out) != 1:
            return False
        return True

    def enable(self):
        self.hset(self._enabled_col, '1')

    def disable(self):
        self.hset(self._enabled_col, '0')

    def hget(self, key):
        return self._user_db.hget(self._user_prefix + self.email, key)

    def last_email(self):
        prev_time = self.hget('last_email')
        if not prev_time:
            return float('0')
        return float(prev_time)

    def set_last_email(self):
        self.hset('last_email', str(time.time()))

    def delete(self):
        self._user_db.delete(self._user_prefix + self.email,
                             self._stat_prefix + self.email,
                             self._api_key_prefix + self.email,
                             self._login_key_prefix + self.email)

    def hset(self, key, val):
        return self._user_db.hset(self._user_prefix + self.email, key, val)

    def create_api_key(self, ttl=86400):
        key = self._key_gen()
        k = self._api_key_prefix + self.email
        cur_time = time.time()
        self._user_db.zremrangebyscore(k, -float('inf'), cur_time)
        self._user_db.zadd(k, str(cur_time + ttl), self._hash_key(key))
        return key

    def create_login_key(self):
        key = self._key_gen()
        self._user_db.set(self._login_key_prefix + self.email, self._hash_key(key))
        return key

    def add_image_prefix(self, prefix, permissions):
        self._user_db.hset(self._image_row_prefix + self.email, prefix, permissions)

    def remove_image_prefix(self, prefix):
        self._user_db.hdel(self._image_row_prefix + self.email, prefix)

    @property
    def image_prefixes(self):
        return self._user_db.hgetall(self._image_row_prefix + self.email)

    @property
    def login_key(self):
        return self._user_db.get(self._login_key_prefix + self.email)

    def verify_api_key(self, key):
        k = self._api_key_prefix + self.email
        self._user_db.zremrangebyscore(k, -float('inf'), time.time())
        out = self._user_db.zscore(k, self._hash_key(key))
        return out is not None

    def verify_login_key(self, key):
        return self.login_key == self._hash_key(key)

    def stats(self):
        return dict((x, self.hget(self._stat_prefix + x)) for x in self._stat_keys)

    @contextlib.contextmanager
    def _api_stats(self):
        self._user_db.hincrby(self._user_prefix + self.email, self._stat_prefix + 'start', 1)
        st = time.time()
        yield
        self._user_db.hincrby(self._user_prefix + self.email, self._stat_prefix + 'finish', 1)
        self._user_db.hincrbyfloat(self._user_prefix + self.email, self._stat_prefix + 'total_time', time.time() - st)
        # TODO: Add min/max response times, compute std

    def _key_gen(self):
        # Replaces +/ with ab so that keys are easily selected, can compensate with keylength
        return base64.b64encode(os.urandom(self.key_length), 'ab')

    def _hash_key(self, key):
        return hashlib.sha512(key).digest()


class Users(object):

    def __init__(self, host, port, db):
        self.user_db = redis.StrictRedis(host=host, port=port, db=db)
        self.email_func = email_auth_factory()

    def add_user(self, email):
        User(self.user_db, email, setup=True)

    def remove_user(self, email):
        self.get_user(email).delete()

    def disable_user(self, email):
        self.get_user(email).disable()

    def enable_user(self, email):
        self.get_user(email).enable()

    def list_users(self):
        return list(set(x.split(':')[1] for x in self.user_db.keys()))

    def get_user(self, email):
        return User(self.user_db, email)

    def verify_api_user(self):
        if bottle.request.auth is None:
            bottle.abort(401)
        try:
            email, api_key = bottle.request.auth
        except ValueError:
            bottle.abort(401)
        print('Email[%s]' % email)
        user = self.get_user(email)
        if not user.verify_api_key(api_key):
            bottle.abort(401)
        return user

    def verify_login_user(self):
        if bottle.request.auth is None:
            bottle.abort(401)
        try:
            email, login_key = bottle.request.auth
        except ValueError:
            bottle.abort(401)
        print('Email[%s]' % email)
        user = self.get_user(email)
        if not user.verify_login_key(login_key):
            bottle.abort(401)
        return user

    def email_api_key(self, user):
        # Can only send one every hour
        if time.time() - user.last_email() >= 3600:
            user.set_last_email()
            self.email_func(user.email, user.create_api_key())

    def email_login_api_key(self, user):
        self.email_func(user.email, user.create_api_key(), user.create_login_key())

    def auth_api_key(self, private=False):
        def inner(func):
            def wrapper(*args, **kw):
                user = self.verify_api_user()
                with user._api_stats():
                    if private:
                        out = func(*args, _auth_user=user, **kw)
                    else:
                        out = func(*args, **kw)
                return out
            return wrapper
        return inner

    def auth_login_key(self, private=False):
        def inner(func):
            def wrapper(*args, **kw):
                user = self.verify_login_user()
                with user._api_stats():
                    if private:
                        out = func(*args, _auth_user=user, **kw)
                    else:
                        out = func(*args, **kw)
                return out
            return wrapper
        return inner


def main():

    def _add_user(args, users):
        for x in args.emails:
            print('Adding user [%s]' % x)
            users.add_user(x)

    def _add_user_image_prefix(args, users):
        user = users.get_user(args.email)
        user.add_image_prefix(args.prefix, args.permissions)

    def _remove_user_image_prefix(args, users):
        user = users.get_user(args.email)
        user.remove_image_prefix(args.prefix)

    def _list_user_image_prefix(args, users):
        user = users.get_user(args.email)
        print user.image_prefixes

    def _auth(args, users):
        user = users.get_user(args.email)
        print user.create_auth(args.ttl)

    def _email_login_api(args, users):
        user = users.get_user(args.email)
        users.email_login_api_key(user)

    def _stats(args, users):
        print(json.dumps(dict((x, users.get_user(x).stats()) for x in users.list_users())))

    def _remove_user(args, users):
        for x in args.emails:
            users.remove_user(x)

    parser = argparse.ArgumentParser(description='Picarus user operations')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6380)
    parser.add_argument('--redis_db', type=int, help='Redis DB', default=0)
    subparsers = parser.add_subparsers(help='Commands')

    subparser = subparsers.add_parser('add_image_prefix', help='Add prefix')
    subparser.add_argument('email', help='email')
    subparser.add_argument('prefix', help='Prefix')
    subparser.add_argument('permissions', help='Permissions')
    subparser.set_defaults(func=_add_user_image_prefix)

    subparser = subparsers.add_parser('remove_image_prefix', help='Remove prefix')
    subparser.add_argument('email', help='email')
    subparser.add_argument('prefix', help='Prefix')
    subparser.set_defaults(func=_remove_user_image_prefix)

    subparser = subparsers.add_parser('list_image_prefix', help='List prefix')
    subparser.add_argument('email', help='email')
    subparser.set_defaults(func=_list_user_image_prefix)

    subparser = subparsers.add_parser('email_login_api', help='Email the user their login/api details')
    subparser.add_argument('email', help='email')
    subparser.set_defaults(func=_email_login_api)

    subparser = subparsers.add_parser('auth', help='Create an auth key for a user')
    subparser.add_argument('email', help='email')
    subparser.add_argument('ttl', help='Time to live (sec)')
    subparser.set_defaults(func=_auth)

    subparser = subparsers.add_parser('add', help='Add users')
    subparser.add_argument('emails', nargs='+', help='emails')
    subparser.set_defaults(func=_add_user)

    subparser = subparsers.add_parser('remove', help='Remove users')
    subparser.add_argument('emails', nargs='+', help='emails')
    subparser.set_defaults(func=_remove_user)

    subparser = subparsers.add_parser('stats', help='Get user stats')
    subparser.set_defaults(func=_stats)
    args = parser.parse_args()
    users = Users(args.redis_host, args.redis_port, args.redis_db)
    args.func(args, users)

if __name__ == '__main__':
    main()
