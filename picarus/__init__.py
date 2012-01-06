__all__ = ['vision', 'cluster', 'report', 'classify', 'io']
from picarus import vision, cluster, report, classify, io
import picarus._file_parse as file_parse
_FROZEN_PATHS = {}  # [script_path] = frozen_path
GLOBAL_JOBCONFS = []


def _freeze_script(script_path):
    import hadoopy
    if script_path not in _FROZEN_PATHS:
        _FROZEN_PATHS[script_path] = hadoopy.freeze_script(script_path)
    return _FROZEN_PATHS[script_path]
        

def _launch_frozen(in_path, out_path, script_path, *args, **kw):
    import hadoopy
    import os
    kw = dict(kw)  # Make a copy as we will be mutating it
    kw['frozen_tar_path'] = _freeze_script(script_path)['frozen_tar_path']
    if 'reducer' not in kw and 'num_reducers' not in kw:
        kw['num_reducers'] = 1
    if 'jobconfs' in kw:
        kw['jobconfs'] = kw['jobconfs'] + GLOBAL_JOBCONFS
    else:
        kw['jobconfs'] = GLOBAL_JOBCONFS
    if 'image_hashes' in kw and kw['image_hashes'] is not None:
        import tempfile
        fp = tempfile.NamedTemporaryFile(suffix='.pkl.gz')
        file_parse.dump(kw['image_hashes'], fp.name)
        try:
            kw['files'].append(fp.name)
        except KeyError:
            kw['files'] = [fp.name]
        try:
            kw['cmdenvs'].append('PICARUS_VALID_IMAGE_HASHES=%s' % os.path.basename(fp.name))
        except KeyError:
            kw['cmdenvs'] = ['PICARUS_VALID_IMAGE_HASHES=%s' % os.path.basename(fp.name)]
        kw['_internal_dummy_arg'] = fp  # Keep the object alive
        del kw['image_hashes']
        
    return hadoopy.launch_frozen(in_path, out_path, script_path, *args, **kw)


def valid_image_check(func):

    def inner(self, k, v):
        try:
            good_input = k in self._picarus_valid_image_hashes
        except AttributeError:
            self._picarus_valid_image_hashes = file_parse.load(os.environ['PICARUS_VALID_IMAGE_HASHES'])
            good_input = k in self._picarus_valid_image_hashes
        if good_input:
            return func(self, k, v)

    import os
    if 'PICARUS_VALID_IMAGE_HASHES' in os.environ:
        return inner
    return func

