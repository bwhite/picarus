import base64
import json
import pickle
import string

VISIBLE_CHARS = None
ISVISIBLE = None


def call_import(import_data):
    """
    Args:
        import_data: Dict
            name:  Import statement for function/class
            args:  Positional arguments to call function with (default [])
            kw:  Keyword arguments to pass (default {})

    Returns:
        Result
    """
    name, attr = import_data['name'].rsplit('.', 1)
    # NOTE(brandyn): the 'arg' makes it give us the most specific module
    m = __import__(name, fromlist=['arg'])
    f = getattr(m, attr)
    return f(*import_data.get('args', []), **import_data.get('kw', {}))


def import_to_name(import_data):
    """
    Args:
        import_data: Dict
            name:  Import statement for function/class
            args:  Positional arguments to call function with (default [])
            kw:  Keyword arguments to pass (default {})

    Returns:
        Result
    """
    global VISIBLE_CHARS, ISVISIBLE
    if VISIBLE_CHARS is None:
        VISIBLE_CHARS = set(string.digits + string.letters + string.punctuation)
        ISVISIBLE = lambda y: all(x in VISIBLE_CHARS for x in y)
    import hashlib
    out = import_data['name']
    
    def arg_to_str(arg):
        if isinstance(arg, (int, float)):
            return json.dumps(arg)
        elif isinstance(arg, (str, unicode)) and (not arg or ISVISIBLE(arg)) and len(arg) <= 16:
            return str(arg)
        else:
            return '(%s)' % base64.urlsafe_b64encode(hashlib.sha1(pickle.dumps(arg)).digest())[:6]
    args = import_data.get('args', [])
    kw = import_data.get('kw', {})
    if args or kw:
        out_args = map(arg_to_str, args)
        out_args += ['%s=%s' % (x, arg_to_str(y)) for x, y in sorted(kw.items())]
    else:
        out_args = []
    out += '(%s)' % ','.join(out_args)
    # Basic sanity checks
    assert out
    assert ' ' not in out
    return out

if __name__ == '__main__':
    print(import_to_name({'name': 'imfeat.Histogram'}))
    print(import_to_name({'name': 'imfeat._histogram.Histogram'}))
    print(import_to_name({'name': 'imfeat.Histogram', 'args': ['rgb', .3131], 'kw': {'num_bins': 8, 'a_string': 'sdfskj', 'b_string': '\n', 'c_string': 'dskfksdjfkjskdfjksjdfksjfdk'}}))
    print call_import({'name': 'imfeat.Histogram', 'args': ['rgb']})
    print(call_import({'name': 'imfeat._object_bank.object_bank.ObjectBank'}))
