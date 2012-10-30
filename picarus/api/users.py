import bottle
import hashlib
import os
import base64
import contextlib
import time


class User(object):

    def __init__(self, user_db, user):
        self._user_db = user_db
        self._user = user
        self._stat_keys = ('start', 'finish', 'total_time')
        self._stat_prefix = 'stat:'

    def hget(self, key):
        return self._user_db.hget(self._user, key)

    @contextlib.contextmanager
    def _api_stats(self):
        self._user_db.hincrby(self._user, self._stat_prefix + 'start', 1)
        st = time.time()
        yield
        self._user_db.hincrby(self._user, self._stat_prefix + 'finish', 1)
        self._user_db.hincrbyfloat(self._user, self._stat_prefix + 'total_time', time.time() - st)
        # TODO: Add min/max response times, compute std

    def stats(self):
        return dict((x, self.hget(self._stat_prefix + x)) for x in self._stat_keys)


class Users(object):

    def __init__(self, user_db):
        self.user_db = user_db
        self.hash_col = 'hash'
        self.key_length = 15
        assert self.key_length % 3 == 0
        assert self.key_length > 0

    def hash_key(self, key):
        return hashlib.sha512(key).digest()

    def key_gen(self):
        return base64.urlsafe_b64encode(os.urandom(self.key_length))

    def add_user(self, user):
        key = self.key_gen()
        self.user_db.hset(user, self.hash_col, self.hash_key(key))
        return key

    def verify_user(self):
        if bottle.request.auth is None:
            bottle.abort(401)
        try:
            user, key = bottle.request.auth
        except ValueError:
            bottle.abort(401)
        if self.user_db.hget(user, self.hash_col) != self.hash_key(key):
            bottle.abort(401)
        return User(self.user_db, user)

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
