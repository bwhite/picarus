#!/usr/bin/env python
# Based on https://code.google.com/p/yubikey-python/source/browse/trunk/decrypt.py
import re
import base64
import Crypto.Cipher.AES
import redis
import json

RE_TOKEN = re.compile(r'^[cbdefghijklnrtuv]{32,64}$')


def _modhex_decode(input):
    it = iter(input)
    chars = 'cbdefghijklnrtuv'
    for first, second in zip(it, it):
        yield chr(chars.index(first) * 16 + chars.index(second))


def _modhex_encode(input):
    chars = 'cbdefghijklnrtuv'
    for i in input:
        v = ord(i)
        yield chars[v // 16]
        yield chars[v % 16]


def _crc_check(decoded):
    m_crc = 0xffff
    for pos in range(0, 16):
        m_crc ^= ord(decoded[pos]) & 0xff
        for i in range(0, 8):
            test = m_crc & 1
            m_crc >>= 1
            if test:
                m_crc ^= 0x8408
    return m_crc == 0xf0b8


def _crc(decoded):
    # From http://static.yubico.com/var/uploads/YubiKey_manual-2.0.pdf
    # Page 25
    m_crc = 0x5af0
    for c in decoded:
        m_crc ^= ord(c) & 0xff
        for i in range(0, 8):
            test = m_crc & 1
            m_crc >>= 1
            if test:
                m_crc ^= 0x8408
    return m_crc


class Yubikey(object):

    def __init__(self, host, port, db):
        self.yubikey_db = redis.StrictRedis(host=host, port=port, db=db)

    def verify(self, input):
        public_id = yubikey_decode_public_id(input)
        if not self.yubikey_db.exists(public_id):
            return
        out = yubikey_decrypt(input, self.yubikey_db.hget(public_id, 'aes_key'))
        if not out or not out['crc_ok']:
            return
        if self.yubikey_db.hget(public_id, 'secret_id') != out['secret_id']:
            return
        # Verify that input is strictly newer than the newest we have seen
        cur_replay_value = int(out['session_counter']), int(out['token_counter'])
        prev_replay_value = int(self.yubikey_db.hget(public_id, 'session_counter')), int(self.yubikey_db.hget(public_id, 'token_counter'))
        if cur_replay_value <= prev_replay_value:
            return
        # We now trust the user is who they say they are, update our codes and produce the "user" data (opaque user ID)
        self.yubikey_db.hmset(public_id, {'session_counter': out['session_counter'], 'token_counter': out['token_counter'], 'timecode': out['timecode']})
        return self.yubikey_db.hget(public_id, 'user')

    def add_yubikey(self, user, public_id, secret_id, aes_key):
        self.yubikey_db.hmset(public_id, {'session_counter': 0, 'timecode': 0, 'token_counter': 0, 'aes_key': aes_key, 'secret_id': secret_id, 'user': user})


def yubikey_decode_public_id(input):
    return ''.join(_modhex_decode(input[:-32]))


def yubikey_decrypt(input, aes_key):
    if not RE_TOKEN.match(input):
        return

    if len(aes_key) != 16:
        return
    out = {}
    out['public_id'] = yubikey_decode_public_id(input)
    token = input[-32:]
    token_bin = ''.join(_modhex_decode(token))
    decoded = Crypto.Cipher.AES.new(aes_key, Crypto.Cipher.AES.MODE_ECB).decrypt(token_bin)
    out['secret_id'] = decoded[0:6]
    out['session_counter'] = ord(decoded[7]) * 256 + ord(decoded[6])
    out['timecode'] = ord(decoded[10]) * 65536 + ord(decoded[9]) * 256 + ord(decoded[8])
    out['timecode_0'] = ord(decoded[8])
    out['timecode_1'] = ord(decoded[9])
    out['timecode_2'] = ord(decoded[10])
    out['token_counter'] = ord(decoded[11])
    out['random_number'] = ord(decoded[13]) * 256 + ord(decoded[12])
    out['crc'] = ord(decoded[15]) * 256 + ord(decoded[14])
    out['crc_ok'] = _crc_check(decoded)
    return out


def yubikey_encrypt(public_id, secret_id, session_counter, timecode, token_counter, random_number, aes_key):
    assert 0 < len(public_id) <= 16
    assert len(aes_key) == 16
    assert len(secret_id) == 6
    assert 0 <= session_counter < 65536
    assert 0 <= timecode < 16777216
    assert 0 <= token_counter < 256
    assert 0 <= random_number < 65536
    decoded = [secret_id]  # [0:6]
    decoded.append(chr(session_counter % 256))   # [6]
    decoded.append(chr(session_counter // 256))  # [7]
    decoded.append(chr(timecode % 256))   # [8]
    decoded.append(chr((timecode // 256) % 256))  # [9]
    decoded.append(chr(timecode // 65536))  # [10]
    decoded.append(chr(token_counter))  # [11]
    decoded.append(chr(random_number % 256))  # [12]
    decoded.append(chr(random_number // 256))  # [13]
    crc = _crc(''.join(decoded))
    print(crc)
    decoded.append(chr(crc % 256))  # [14]
    decoded.append(chr(crc // 256))  # [15]
    decoded = ''.join(decoded)
    token = ''.join(_modhex_encode(Crypto.Cipher.AES.new(aes_key, Crypto.Cipher.AES.MODE_ECB).encrypt(decoded)))
    assert len(token) == 32
    return ''.join(_modhex_encode(public_id)) + token


def main():
    def _add_yubikey(args):
        yk = Yubikey(args.redis_host, args.redis_port, 1)
        yk.add_yubikey(args.user, base64.b64decode(args.public_id), base64.b64decode(args.secret_id), base64.b64decode(args.aes_key))

    def _verify(args):
        yk = Yubikey(args.redis_host, args.redis_port, 1)
        print yk.verify(args.input)

    def _encrypt(args):
        vargs = vars(args)
        del vargs['func']
        del vargs['redis_host']
        del vargs['redis_port']
        for k in ['public_id', 'secret_id', 'aes_key']:
            vargs[k] = base64.b64decode(vargs[k])
        otp = yubikey_encrypt(**vargs)
        # Check that it decrypts ok
        out = yubikey_decrypt(otp, args.aes_key)
        assert out['public_id'] == args.public_id
        assert out['secret_id'] == args.secret_id
        assert out['timecode'] == args.timecode
        assert out['token_counter'] == args.token_counter
        assert out['random_number'] == args.random_number
        assert out['crc_ok']
        print(json.dumps({'otp': otp}))

    import argparse
    parser = argparse.ArgumentParser(description='Picarus yubikey operations')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6379)
    subparsers = parser.add_subparsers(help='Commands')

    subparser = subparsers.add_parser('add', help='Add yubikey')
    subparser.add_argument('user', help='Opaque User ID')
    subparser.add_argument('public_id', help='Public ID (b64 encoded)')
    subparser.add_argument('secret_id', help='Private ID (b64 encoded)')
    subparser.add_argument('aes_key', help='AES Key (b64 encoded)')
    subparser.set_defaults(func=_add_yubikey)

    subparser = subparsers.add_parser('verify', help='Verify otp')
    subparser.add_argument('input', help='OTP Input')
    subparser.set_defaults(func=_verify)

    subparser = subparsers.add_parser('encrypt', help='Generate an otp from parts (for testing purposes)')
    subparser.add_argument('public_id', help='(0, 16] bytes (b64 encoded)')
    subparser.add_argument('secret_id', help='6 binary bytes (b64 encoded)')
    subparser.add_argument('aes_key', help='16 binary bytes (b64 encoded)')
    subparser.add_argument('session_counter', type=int, help='0 <= x < 65536')
    subparser.add_argument('token_counter', type=int, help='0 <= x < 256')
    subparser.add_argument('timecode', type=int, help='0 <= x < 16777216')
    subparser.add_argument('random_number', type=int, help='0 <= x < 65536')
    subparser.set_defaults(func=_encrypt)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
