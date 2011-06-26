import hadoopy
import vidfeat
import os
import picarus
import hashlib


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def _sha1(fn, chunk_size=1048576):
    h = hashlib.sha1()
    data = open(fn)
    while 1:
        chunk = data.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()
        

def _read_files(fns, prev_hashes, hdfs_output, output_format, max_record_size):
    """
    Args:
        fns: Iterator of file names
        prev_hashes: Set of hashes (they will be skipped), this is used to make
            the data unique

    Yields:
        Tuple of (data_hash, data) where data_hash is a sha1 hash
    """
    for fn in fns:
        sha1_hash = _sha1(fn)
        if sha1_hash not in prev_hashes:
            prev_hashes.add(sha1_hash)
            if output_format == 'record' and max_record_size is not None and max_record_size < os.stat(fn)[6]:
                # Put the file into the remote location
                hdfs_path = '%s/blobs/%s_%s' % (hdfs_output, sha1_hash, os.path.basename(fn))
                data = ''
                hadoopy.put(fn, hdfs_path)
            else:
                hdfs_path = ''
                data = open(fn).read()
            if output_format == 'kv':
                yield sha1_hash, data
            elif output_format == 'record':
                out = {'sha1': sha1_hash, 'full_path': fn,
                       'extension': os.path.splitext(fn)[1][1:]}
                if data:
                    out['data'] = data
                if hdfs_path:
                    out['hdfs_path'] = hdfs_path
                yield sha1_hash, out


def load_local(local_input, hdfs_output, output_format='kv', max_record_size=None, **kw):
    """Read data, de-duplicate, and put on HDFS in the specified format

    Args:
        local_input: Local directory path
        hdfs_output: HDFS output path
        output_format: One of 'kv' or 'record'.  If 'kv' then output one
            sequence file of the form (sha1_hash, binary_file_data).  If 'record'
            make a directory at the hdfs_output path and put inside one sequence
            file called 'records' of the form (sha1_hash, metadata)

            where metadata has keys
            sha1: Sha1 hash
            extension: File extension without a period (blah.avi -> avi,
                blah.foo.avi -> avi, blah -> '')
            full_path: Local file path
            hdfs_path: HDFS path of the file (if any), the data should be the
                binary contents of the file stored at this location on HDFS.
            data: Binary file contents

            where only one of data or hdfs_path has to exist.
        max_record_size: If using 'record' and the filesize (in bytes) is larger
            than this, then store the contents of the file in a directory called
            'blobs' inside output path with the name as the sha1 hash prefixed
            to the original file name (example, hdfs_output/blobs/sha1hash_origname).
            If None then there is no limit to the record size (default is None).
    """
    fns = sorted([os.path.join(local_input, x) for x in os.listdir(local_input)])
    if output_format == 'kv':
        output_path = hdfs_output
    elif output_format == 'record':
        output_path = hdfs_output + '/records'
    else:
        raise ValueError('Unsupported output_format [%s]' % output_format)
    hadoopy.writetb(output_path, _read_files(fns, set(), hdfs_output, output_format, max_record_size))


def dump_local(hdfs_input, local_output, extension='', **kw):
    """Read data from hdfs and store the contents as hash.ext

    Args:
        hdfs_input: HDFS input path in either 'kv' or 'record' format
        local_output: Local directory output path
        extension: Use this file extension if none available (kv format or
            record with missing extension) (default '')
    """
    try:
        os.makedirs(local_output)
    except OSError:
        pass
    for k, v in hadoopy.readtb(hdfs_input):
        fn = k
        data = None
        hdfs_path = None
        if isinstance(v, dict):  # record
            try:
                extension = v['extension']
            except KeyError:
                pass
            try:
                data = v['data']
            except KeyError:
                try:
                    hdfs_path = v['hdfs_path']
                except KeyError:
                    pass
        elif isinstance(v, str):
            data = v
        else:
            raise ValueError('Value must be either a dict or a string.')
        if extension:
            fn += '.%s' % extension
        out_path = os.path.join(local_output, fn)
        if data is not None:
            with open(out_path, 'wb') as fp:
                fp.write(data)
        elif hdfs_path is not None:
            hadoopy.get(hdfs_path, out_path)
        else:
            raise ValueError("Can't find data or hdfs_path, at least one is required.")


def _parser(sps):
    import picarus.__main__
    ca = picarus.__main__._ca
    # Load from local directory
    s = sps.add_parser('load_local', help='Writes data in a (key, value) format to hdfs')
    s.add_argument('local_input', help='Local input directory path (all files in directory used)')
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('--output_format', help=("Data format to use.  'kv': (sha1_hash, binary_data) or 'record'"
                                            " (sha1_hash, metadata) (see docstring) (default 'kv')"), default='kv')
    s.add_argument('--max_record_size', help="If using record format, larger files are placed directly on HDFS (see docstring) (default None)", default=None)
    s.set_defaults(func=picarus.io.load_local)

    # Dump to local directory
    s = sps.add_parser('dump_local', help='Writes data as local_output/sha1hash.ext')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('local_output', help='Local output directory path (created if not there)')
    s.add_argument('--extension', help="Extension to give output files, only used if not provided by the data. (default '')")
    s.set_defaults(func=picarus.io.dump_local)


