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

    def email_func(email, auth):
        conn = boto.connect_ses(EMAIL['key'], EMAIL['secret'])
        auth_link = EMAIL['url'] + '?email=%s&auth=%s' % (email, auth)
        return conn.send_email(source=EMAIL['admin'], subject='[%s] - Login Link' % EMAIL['name'],
                               body='<a href="%s">Login</a><br>Email: %s' % (auth_link, email), to_addresses=email, format='html')
    return email_func


def captcha_factory(captcha_fn='recaptcha.js'):
    recaptcha = json.load(open(captcha_fn))  # keys as key, secret, admin, url, name
    import requests

    def captcha(remoteip, challenge, response):
        r = requests.post('https://www.google.com/recaptcha/api/verify', data={'privatekey': recaptcha['privatekey'],
                                                                               'remoteip': remoteip,
                                                                               'challenge': challenge,
                                                                               'response': response})
        return r.content.split('\n')
    return captcha


class UnknownUser(Exception):
    """User not in the database"""


class User(object):
    """Picarus User Class

    Public Methods: Safe to use from frontend
    Private Methods: Should not be used in frontend
    """

    def __init__(self, user_db, user, setup=False):
        self._user_db = user_db
        self.user = user
        self._stat_keys = ('start', 'finish', 'total_time')
        self._user_prefix = 'user:'
        self._stat_prefix = 'stat:'
        self._auth_prefix = 'auth:'
        self._enabled_col = 'enabled'
        self.key_length = 15
        assert self.key_length % 3 == 0
        assert self.key_length > 0
        if setup:
            self.enable()
        if not self._exists():
            raise UnknownUser

    def _exists(self):
        return self._user_db.exists(self._user_prefix + self.user) == 1

    def enabled(self):
        out = self.hget(self._user_prefix + self.user, self._enabled_col)
        if out is None or int(out) != 1:
            return False
        return True

    def enable(self):
        self.hset(self._enabled_col, '1')

    def disable(self):
        self.hset(self._enabled_col, '0')

    def hget(self, key):
        return self._user_db.hget(self._user_prefix + self.user, key)

    def delete(self):
        self.user_db.delete(self._user_prefix + self.user,
                            self._stat_prefix + self.user,
                            self._auth_prefix + self.user)

    def hset(self, key, val):
        return self._user_db.hset(self._user_prefix + self.user, key, val)

    def create_auth(self):
        key = self._key_gen()
        self._user_db.zadd(self._auth_prefix + self.user, str(time.time()), self._hash_key(key))
        return key

    def verify(self, key, min_time=0.):
        out = self._user_db.zscore(self._auth_prefix + self.user, self._hash_key(key))
        print(out)
        return out is not None and float(out) >= min_time

    def stats(self):
        return dict((x, self.hget(self._stat_prefix + x)) for x in self._stat_keys)

    @contextlib.contextmanager
    def _api_stats(self):
        self._user_db.hincrby(self._user_prefix + self.user, self._stat_prefix + 'start', 1)
        st = time.time()
        yield
        self._user_db.hincrby(self._user_prefix + self.user, self._stat_prefix + 'finish', 1)
        self._user_db.hincrbyfloat(self._user_prefix + self.user, self._stat_prefix + 'total_time', time.time() - st)
        # TODO: Add min/max response times, compute std

    def _key_gen(self):
        return base64.urlsafe_b64encode(os.urandom(self.key_length))

    def _hash_key(self, key):
        return hashlib.sha512(key).digest()


class Users(object):

    def __init__(self, host, port, db):
        self.user_db = redis.StrictRedis(host=host, port=port, db=db)
        self.email_func = email_auth_factory()
        self.captcha_func = captcha_factory()

    def add_user(self, user):
        User(self.user_db, user, setup=True)

    def remove_user(self, user):
        User(self.user_db, user).delete()

    def disable_user(self, user):
        User(self.user_db, user).disable()

    def enable_user(self, user):
        User(self.user_db, user).enable()

    def list_users(self):
        return list(set(x.split(':')[1] for x in self.user_db.keys()))

    def get_user(self, user):
        return User(self.user_db, user)

    def verify_user(self):
        if bottle.request.auth is None:
            bottle.abort(401)
        try:
            user, key = bottle.request.auth
        except ValueError:
            bottle.abort(401)
        print('User[%s]' % user)
        auth_user = self.get_user(user)
        if not auth_user.verify(key):
            bottle.abort(401)
        return auth_user

    def email_auth(self, email, remoteip, challenge, response):
        out = self.captcha_func(remoteip, challenge, response)
        if out[0] != 'true':
            bottle.abort(401, 'Incorrect captcha')
        cur_auth = User(self.user_db, email).create_auth()
        print('Emailing[%s] [%s]' % (email, cur_auth))
        self.email_func(email, cur_auth)

    def auth(self, private=False):
        def inner(func):
            def wrapper(*args, **kw):
                auth_user = self.verify_user()
                with auth_user._api_stats():
                    if private:
                        out = func(*args, auth_user=auth_user, **kw)
                    else:
                        out = func(*args, **kw)
                return out
            return wrapper
        return inner


def main():
    def _add_user(args, users):
        for x in args.users:
            print('Adding user [%s]' % x)
            users.add_user(x)

    def _stats(args, users):
        print(json.dumps(dict((x, users.get_user(x).stats()) for x in users.list_users())))

    def _remove_user(args, users):
        for x in args.users:
            users.remove_user(x)

    parser = argparse.ArgumentParser(description='Picarus user operations')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6380)
    parser.add_argument('--redis_db', type=int, help='Redis DB', default=0)
    subparsers = parser.add_subparsers(help='Commands')
    subparser = subparsers.add_parser('add', help='Add users')
    subparser.add_argument('users', nargs='+', help='Users')
    subparser.set_defaults(func=_add_user)
    subparser = subparsers.add_parser('remove', help='Add users')
    subparser.add_argument('users', nargs='+', help='Users')
    subparser.set_defaults(func=_remove_user)
    subparser = subparsers.add_parser('stats', help='Get user stats')
    subparser.set_defaults(func=_stats)
    args = parser.parse_args()
    users = Users(args.redis_host, args.redis_port, args.redis_db)
    args.func(args, users)

if __name__ == '__main__':
    main()
