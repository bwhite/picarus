import heapq
import hadoopy
import os
import cStringIO as StringIO
import Image
import re
import random
from picarus import _file_parse as file_parse
from picarus.report import report_output
import picarus
import json


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def _parser(sps):
    import picarus.__main__
    ca = picarus.__main__._ca

    # Report Clustering
    s = sps.add_parser('clusters', help='Report Clusters')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('local_json_output', help='report output')
    s.add_argument('category', help='category tag for this clustering')
    s.add_argument('--sample', help='sample size', type=int, default=20)
    s.add_argument('--make_faces', action="store_true", help='set this for face clusters')
    s.set_defaults(func=_report_clusters)

    # Make Thumbnails
    s = sps.add_parser('make_thumbnails', help='Make Thumbnails')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('thumb_size', help='thumbnail width in pixels', type=int)
    s.add_argument('--is_cluster', help='used to indicate the samples output from a clustering')
    s.set_defaults(func=make_thumbnails)

    # Local Thumbnail Output
    s = sps.add_parser('thumbnails', help='Report Categories from Face Clustering')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('local_thumb_output', help='local thumbnail output directory')
    s.set_defaults(func=report_thumbnails)

    # Report Video Keyframes
    s = sps.add_parser('video_keyframe', help='Report Video Keyframes')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('local_json_output', help='local json report output')
    s.add_argument('--local_thumb_output', help='local thumbnail output directory')
    s.set_defaults(func=_report_video_keyframe)


def report_clusters(hdfs_input, sample, category, make_faces, **kw):
    """
    NOTE: This transfers much more image data than is necessary! Really this operation
    should be done directly on hdfs
    """
    def make_face_image(facestr):
        name, ext = os.path.splitext(facestr)
        m = re.match('(\w+)-face-x0(\d+)-y0(\d+)-x1(\d+)-y1(\d+)', name)
        hash, l, t, r, b = m.groups()
        l, t, r, b = map(int, (l, t, r, b))
        #m = re.match('(\w+)-face-x0(\d+)-y0(\d+)-x1(\d+)-y1(\d+)', name)
        #hash, l, t, r, b = m.groups()
        return {
            'hash': hash,
            'categories': ['faces'],
            'faces': [{'boundingbox': ((l, t), (r, b))}],
            'video': [],
        }

    # Collect all the clusters as a set of lists
    clusters = {}
    for cluster_index, (image_name, _)  in hadoopy.readtb(hdfs_input):
        cluster = clusters.setdefault(cluster_index, [])
        if make_faces:
            face_image = make_face_image(image_name)
            cluster.append(face_image)
        else:
            cluster.append({
                'hash': image_name,
                'categories': [category],
                'faces': [],
                'video': [],
                })

    # Gather each cluster
    if not sample:
        sample = float('inf')
    clusters = [{
        # Sample images uniformly
        'sample_images': random.sample(image_set, min(len(image_set), sample)),
        'all_images': image_set,
        'size': len(image_set),
        'children': [],
        'std': 0.0,
        'position': [0.0, 0.0],
        } for image_set in clusters.values()]

    report = {category: clusters}
    return report


def _report_clusters(hdfs_input, local_json_output, sample, category, make_faces, **kw):
    report = report_clusters(hdfs_input, sample, category, make_faces, **kw)
    file_parse.dump(report, local_json_output)


def make_thumbnails(hdfs_input, hdfs_output, thumb_size, is_cluster=False, **kw):
    script = 'make_thumbnails.py' if not is_cluster else 'make_cluster_thumbnails.py'
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf(script),
                          reducer=None,
                          cmdenvs=['THUMB_SIZE=%d' % thumb_size])


def report_thumbnails(hdfs_input, local_thumb_output, **kw):
    """Collect thumbnails of all images in hdfs://${hdfs_input}
    """
    try:
        os.makedirs(local_thumb_output)
    except OSError:
        pass
    counter = 0
    for image_hash, image_data in hadoopy.readtb(hdfs_input):
        path = '%s/%s.jpg' % (local_thumb_output, image_hash)
        with open(path, 'w') as f:
            f.write(image_data)
        counter += 1
    if not counter:
        print 'There were no images in readtb(%s). This is probably not a thumbnail path' % hdfs_input


def report_video_keyframe(hdfs_input, **kw):
    videos = {}
    for (kind, hash), v in hadoopy.readtb(hdfs_input):
        if kind == 'video':
            videos[hash] = v
    if not len(videos):
        # Sanity check
        print "No videos returned by readtb(%s). This is probably the wrong keyframe path" % hdfs_input
    report = {'videos': videos}
    return report


def _report_video_keyframe(hdfs_input, local_json_output, **kw):
    report = report_video_keyframe(hdfs_input)
    file_parse.dump(report, local_json_output)
