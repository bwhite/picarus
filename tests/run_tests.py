import os
import subprocess
import argparse
import random
import json
import base64
import vision_data
import tempfile


def parse():
    parser = argparse.ArgumentParser(description='Picarus Test Suite')
    parser.add_argument('email')
    parser.add_argument('images_prefix', help='Prefix for the images table')
    parser.add_argument('--api_key')
    parser.add_argument('--login_key')
    parser.add_argument('--otp', action='append')
    parser.add_argument('--setup_user', action='store_true')
    parser.add_argument('--picarus_server', default='http://localhost')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6379)
    parser.add_argument('--root', help='Root path of picarus directory (e.g., .. if pwd is tests or . if pwd is root)', default='..')
    return vars(parser.parse_args())


def _key_gen():
    return base64.b64encode(os.urandom(15), 'ab')


def setup(args):
    print(args)
    num_otp = 2
    args['root'] = os.path.abspath(args['root']) + '/'
    if (args['login_key'] is None or args['api_key'] is None or len(args['otp']) < num_otp) and not args['setup_user']:
        raise ValueError('Must specify login_key/api_key and |otp| >= num_otp if setup_user=False' % num_otp)
    if args['login_key'] is None:
        args['login_key'] = _key_gen()
    if args['api_key'] is None:
        args['api_key'] = _key_gen()
    if args['setup_user']:
        # Allow script to be executed in picarus or picarus/tests
        users_script, yubikey_script = args['root'] + 'server/users.py', args['root'] + 'server/yubikey.py'
        assert os.path.exists(users_script) and os.path.exists(yubikey_script)
        redis_args = ['--redis_host', args['redis_host'], '--redis_port', str(args['redis_port'])]
        users_func = lambda x: subprocess.call([users_script] + redis_args + x.split())
        yubikey_func = lambda x: subprocess.Popen([yubikey_script] + redis_args + x.split(), stdout=subprocess.PIPE).communicate()[0]
        users_func('add %s --noemail' % args['email'])
        users_func('force_login_key %s %s' % (args['email'], args['login_key']))
        users_func('force_api_key %s 86400 %s' % (args['email'], args['api_key']))
        users_func('add_prefix images %s %s rw' % (args['email'], args['images_prefix']))

        # Here we have a "fake" yubikey that we add to the database and generate enough codes for our purposes
        def yubikey_iter():
            public_id = base64.b64encode(os.urandom(8))
            aes_key = base64.b64encode(os.urandom(16))
            secret_id = base64.b64encode(os.urandom(6))
            session_counter = 0
            token_counter = 0
            timecode = 0
            yubikey_func('add %s %s %s %s' % (args['email'], public_id, secret_id, aes_key))
            while session_counter < 65535:
                session_counter += 1
                timecode += 1
                random_number = random.randint(0, 65535)
                print('encrypt %s %s %s %d %d %d %d' % (public_id, secret_id, aes_key, session_counter, token_counter, timecode, random_number))
                yield str(json.loads(yubikey_func('encrypt %s %s %s %d %d %d %d' % (public_id, secret_id, aes_key, session_counter, token_counter, timecode, random_number)))['otp'])
        args['otp'] = [otp for _, otp in zip(range(num_otp), yubikey_iter())]
        print(args)


def load_data(args):
    os.environ['VISION_DATA_ROOT'] = tempfile.mkdtemp()
    vision_data.picarus_loader(args['images_prefix'] + 'caltech256:', 'Caltech256', args['email'], args['picarus_server'], args['api_key'], download=True)


def run(args):
    env = dict(os.environ)
    env.update({'EMAIL': args['email'],
                'LOGIN_KEY': args['login_key'],
                'API_KEY': args['api_key'],
                'OTP': args['otp'][0],
                'SERVER': args['picarus_server']})
    assert subprocess.Popen(['python', args['root'] + 'tests/test_docs.py'], env=env).wait() == 0
    os.chdir(args['root'] + 'tests/casperjs/bin')
    cmd = './casperjs picarus.js --server=%s --email=%s --login_key=%s --api_key=%s --otp=%s' % (args['picarus_server'], args['email'], args['login_key'],
                                                                                                 args['api_key'], args['otp'][1])
    assert subprocess.Popen(cmd.split()).wait() == 0


def main():
    args = parse()
    setup(args)
    load_data(args)
    run(args)

if __name__ == '__main__':
    main()
