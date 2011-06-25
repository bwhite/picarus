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


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def report_clusters(hdfs_input, sample, category, make_faces, **kw):
    """
    NOTE: This transfers much more image data than is necessary! Really this operation
    should be done directly on hdfs
    """
    def make_face_image(facestr):
        name, ext = os.path.splitext(facestr)
        m = re.match('(\w+)-face-x0(\d+)-y0(\d+)-x1(\d+)-y1(\d+)', name)
        print name
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
    count = 0
    for cluster_index, (image_name, _)  in hadoopy.readtb(hdfs_input):
        count += 1
        if count % 100 == 0:
            print(count)
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
    print len(clusters), 'clusters'
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
    print 'about to read', hdfs_input
    for image_hash, image_data in hadoopy.readtb(hdfs_input):
        path = '%s/%s.jpg' % (local_thumb_output, image_hash)
        with open(path, 'w') as f:
            f.write(image_data)
    print 'done reading', hdfs_input


def report_video_keyframe(hdfs_input, **kw):
    videos = {}
    for (kind, hash), v in hadoopy.readtb(hdfs_input):
        if kind == 'video':
            videos[hash] = v
    report = {'videos': videos}
    return report
