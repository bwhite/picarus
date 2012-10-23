import heapq
import hadoopy
import os
import cStringIO as StringIO
from PIL import Image
import re
import random
from picarus import _file_parse as file_parse
import picarus
import json


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def report_clusters(hdfs_input, category, make_faces, **kw):
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
    cluster_samples = {}

    def update(cluster_index, image_name, clusters):
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

    for cluster_index, (image_name, _)  in hadoopy.readtb(hdfs_input + '/partition'):
        update(cluster_index, image_name, clusters)

    for cluster_index, (image_name, _)  in hadoopy.readtb(hdfs_input + '/samples'):
        update(cluster_index, image_name, cluster_samples)

    # Gather each cluster
    clusters = [{
        # Sample images uniformly
        'sample_images': samples,
        'all_images': images,
        'size': len(images),
        'children': [],
        'std': 0.0,
        'position': [0.0, 0.0],
        } for ((_, images), (_, samples)) in zip(sorted(clusters.items()),
                                                 sorted(cluster_samples.items()))]

    report = {category: clusters}
    return report


def _report_clusters(hdfs_input, local_json_output, category, make_faces, **kw):
    report = report_clusters(hdfs_input, category, make_faces, **kw)
    file_parse.dump(report, local_json_output)


def make_thumbnails(hdfs_input, hdfs_output, thumb_size, image_type, **kw):
    script = 'make_thumbnails.py'
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf(script),
                          cmdenvs=['THUMB_SIZE=%d' % thumb_size,
                                   'IMAGE_TYPE=%s' % image_type])


def report_thumbnails(hdfs_input, local_thumb_output, **kw):
    """Collect thumbnails of all images in hdfs://${hdfs_input}
    """
    counter = 0
    for image_hash, image_data in hadoopy.readtb(hdfs_input):
        path = '%s/%s/%s/%s.jpg' % (local_thumb_output,
                                    image_hash[:2],
                                    image_hash[2:4],
                                    image_hash)
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass

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
