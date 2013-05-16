import bottle
import hashlib
import os
import base64
import contextlib
import time
import redis
import argparse
import json
import logging
import re


def email_auth_factory(email_auth_fn='email_auth.js'):
    try:
        EMAIL = json.load(open(email_auth_fn))  # keys as key, secret, admin, url, name
    except IOError:
        EMAIL = {'name': 'Demo picar.us server'}

    def basic_email_func(email, api_key, ttl, login_key=None):
        print('Send the following to: %s' % email)
        if login_key is None:
            body = '<h2>Email</h2><pre>%s</pre><h2><h2>API Key (Expires in %d seconds)</h2><pre>%s</pre>' % (email, ttl, api_key)
            subject = '[%s] - API Key' % EMAIL['name']
        else:
            body = '<h2>Email</h2><pre>%s</pre><h2>Login Key</h2><pre>%s</pre><h2>API Key (Expires in %d seconds)</h2><pre>%s</pre>' % (email, login_key, ttl, api_key)
            subject = '[%s] - Login/API Key' % EMAIL['name']
        print('Subject\n')
        print(subject)
        print('Body\n')
        print(body)

    if not EMAIL.get('key') or not EMAIL.get('secret'):
        logging.warn('Basic email mode as no amazon API key is in email_auth.js, see email_auth.example.js')
        return basic_email_func

    import boto

    def email_func(email, api_key, ttl, login_key=None):
        conn = boto.connect_ses(EMAIL['key'], EMAIL['secret'])
        if login_key is None:
            body = '<h2>Email</h2><pre>%s</pre><h2><h2>API Key (Expires in %d seconds)</h2><pre>%s</pre>' % (email, ttl, api_key)
            subject = '[%s] - API Key' % EMAIL['name']
        else:
            body = '<h2>Email</h2><pre>%s</pre><h2>Login Key</h2><pre>%s</pre><h2>API Key (Expires in %d seconds)</h2><pre>%s</pre>' % (email, login_key, ttl, api_key)
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
        self.upload_row_prefix = 'userupload%s:' % base64.urlsafe_b64encode(hashlib.sha1(email).digest())[:-1]
        self._user_prefix = 'user:'
        self._usage_prefix = 'usage:'
        self._api_key_prefix = 'auth:'
        self._login_key_prefix = 'login:'
        self._enabled_col = 'enabled'
        self.key_length = 15
        self._tables = ('images',)
        assert self.key_length % 3 == 0
        assert self.key_length > 0
        if setup:
            self.enable()
        if not self._exists():
            raise UnknownUser
        self._user_db.delete('stat:' + self.email)

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
                             self._usage_prefix + self.email,
                             self._api_key_prefix + self.email,
                             self._login_key_prefix + self.email)

    def hset(self, key, val):
        return self._user_db.hset(self._user_prefix + self.email, key, val)

    def create_api_key(self, ttl=None):
        if ttl is None:
            ttl = 86400
        ttl = max(1, min(int(ttl), 604800))  # 1sec <= x <= 1week
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

    def _table_prefix(self, table):
        # TODO: was 'image_prefix:' is now 'prefix_images'
        # Fix: a=redis.StrictRedis(port=6380)
        # [a.hmset('prefix_images:' + x.split(':', 1)[1], a.hgetall(x)) for x in a.keys('*_prefix:*')]
        assert table in self._tables
        return 'prefix_%s:' % table

    def _table_project(self, table):
        assert table in self._tables
        return 'project_%s:' % table

    def add_prefix(self, table, prefix, permissions):
        self._user_db.hset(self._table_prefix(table) + self.email, prefix, permissions)

    def remove_prefix(self, table, prefix):
        self._user_db.hdel(self._table_prefix(table) + self.email, prefix)

    def add_project(self, table, project, slices):
        self._user_db.hset(self._table_project(table) + self.email, project, slices)

    def remove_project(self, table, project):
        self._user_db.hdel(self._table_project(table) + self.email, project)

    def prefixes(self, table):
        return self._user_db.hgetall(self._table_prefix(table) + self.email)

    def projects(self, table):
        return self._user_db.hgetall(self._table_project(table) + self.email)

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

    def _sanitize_path(self):
        r = re.search('(/[^/]+/data/[^/]+)', bottle.request.path)
        if r:
            return r.group(1)
        r = re.search('(/[^/]+/data/[^/]+/)[^/]+', bottle.request.path)
        if r:
            return r.group(1) + ':row'
        r = re.search('(/[^/]+/data/[^/]+/)[^/]+/[^/]+', bottle.request.path)
        if r:
            return r.group(1) + ':row/:column'
        r = re.search('(/[^/]+/slice/[^/]+/)[^/]+/[^/]+', bottle.request.path)
        if r:
            return r.group(1) + ':startRow/:stopRow'
        return bottle.request.path

    @contextlib.contextmanager
    def _api_stats(self):
        path_sanitized = self._sanitize_path()
        out = {'method': bottle.request.method, 'path': bottle.request.path}
        if path_sanitized:
            out['pathSanitized'] = path_sanitized
        st = time.time()
        status_code = 200
        try:
            yield
        except bottle.HTTPError, e:
            status_code = e.status_code
            raise
        finally:
            out['time'] = time.time() - st
            out['status_code'] = status_code
            self._user_db.lpush(self._usage_prefix + self.email, json.dumps(out))
            self._user_db.ltrim(self._usage_prefix + self.email, 0, 100000)

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
        return User(self.user_db, email, setup=True)

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

    def email_api_key(self, user, ttl=None):
        if ttl is None:
            ttl = 86400
        # Can only send one every hour
        if time.time() - user.last_email() >= 3600:
            user.set_last_email()
            self.email_func(user.email, user.create_api_key(ttl=ttl), ttl)

    def email_login_api_key(self, user, ttl=None):
        if ttl is None:
            ttl = 86400
        self.email_func(user.email, user.create_api_key(ttl=ttl), ttl, user.create_login_key())

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
            user = users.add_user(x)
            for x in user._tables:
                user.add_prefix(x, user.upload_row_prefix, 'rw')
                user.add_prefix(x, user.upload_row_prefix, 'rw')
            users.email_login_api_key(user)

    def _add_user_prefix(args, users):
        user = users.get_user(args.email)
        user.add_prefix(args.table, args.prefix, args.permissions)

    def _add_upload_prefix(args, users):
        user = users.get_user(args.email)
        for x in user._tables:
            user.add_prefix(x, user.upload_row_prefix, 'rw')
            user.add_prefix(x, user.upload_row_prefix, 'rw')

    def _remove_user_prefix(args, users):
        user = users.get_user(args.email)
        user.remove_prefix(args.table, args.prefix)

    def _list_user_prefix(args, users):
        user = users.get_user(args.email)
        for x in user._tables:
            print('%s: %r' % (x, user.prefixes(x)))

    def _api_key(args, users):
        user = users.get_user(args.email)
        print user.create_api_key(args.ttl)

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

    subparser = subparsers.add_parser('add_prefix', help='Add prefix')
    subparser.add_argument('table', help='table')
    subparser.add_argument('email', help='email')
    subparser.add_argument('prefix', help='Prefix')
    subparser.add_argument('permissions', help='Permissions')
    subparser.set_defaults(func=_add_user_prefix)

    subparser = subparsers.add_parser('add_upload_prefix', help='Add upload prefix')
    subparser.add_argument('email', help='email')
    subparser.set_defaults(func=_add_upload_prefix)

    subparser = subparsers.add_parser('remove_prefix', help='Remove prefix')
    subparser.add_argument('table', help='table')
    subparser.add_argument('email', help='email')
    subparser.add_argument('prefix', help='Prefix')
    subparser.set_defaults(func=_remove_user_prefix)

    subparser = subparsers.add_parser('list_prefix', help='List prefix')
    subparser.add_argument('email', help='email')
    subparser.set_defaults(func=_list_user_prefix)

    subparser = subparsers.add_parser('email_login_api', help='Email the user their login/api details')
    subparser.add_argument('email', help='email')
    subparser.set_defaults(func=_email_login_api)

    subparser = subparsers.add_parser('api_key', help='Create an api_key key for a user')
    subparser.add_argument('email', help='email')
    subparser.add_argument('ttl', help='Time to live (sec)')
    subparser.set_defaults(func=_api_key)

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
