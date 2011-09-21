__all__ = ['vision', 'cluster', 'report', 'classify', 'io']
from picarus import vision, cluster, report, classify, io
import picarus._file_parse as file_parse
_FROZEN_PATHS = {}


def _freeze_script(script_path):
    import hadoopy
    if script_path not in _FROZEN_PATHS:
        _FROZEN_PATHS[script_path] = hadoopy.freeze_script(script_path)
    return _FROZEN_PATHS[script_path]
        

def _launch_frozen(in_path, out_path, script_path, *args, **kw):
    import hadoopy
    kw['frozen_tar_path'] = _freeze_script(script_path)['frozen_tar_path']
    if 'reducer' not in kw and 'num_reducers' not in kw:
        kw['num_reducers'] = 1
    return hadoopy.launch_frozen(in_path, out_path, script_path, *args, **kw)
