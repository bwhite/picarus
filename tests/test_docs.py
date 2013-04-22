try:
    import unittest2 as unittest
except ImportError:
    import unittest

def parse_tests(fn, language='python'):
    pattern = '.. code-block:: %s' % language
    with open(fn) as fp:
        try:
            while 1:
                ln = fp.next()
                if ln.startswith(pattern):
                    code = []
                    fp.next()  # next line is blank
                    ln = fp.next().rstrip()[4:]
                    while ln:
                        code.append(ln)
                        ln = fp.next().rstrip()[4:]
                    yield code
        except StopIteration:
            return


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_docs(self):
        import glob
        import os
        import picarus
        email = os.environ['EMAIL']
        login_key = os.environ['LOGIN_KEY']
        if 'API_KEY' not in os.environ:
            otp = raw_input('Yubikey OTP: ')
            api_key = picarus.PicarusClient(email=email, login_key=login_key).auth_yubikey(otp)['apiKey']
        else:
            api_key = os.environ['API_KEY']
        prefix = ['import picarus']

        def test_passed():
            print('\033[92mTest Passed\033[0m')

        def test_failed():
            print('\033[91mTest Failed\033[0m')
        otp = raw_input('Yubikey OTP: ')
        for doc_fn in glob.glob('../doc/*.rst'):
            for source in parse_tests(doc_fn):
                source = '\n'.join(prefix + source)
                print('Test from file [%s]' % doc_fn)
                print(source)
                exec(compile(source, 'blah.py', 'exec'), {}, {'email': email,
                                                              'login_key': login_key,
                                                              'api_key': api_key,
                                                              'otp': otp,
                                                              'test_passed': test_passed,
                                                              'test_failed': test_failed})

if __name__ == '__main__':
    unittest.main()
