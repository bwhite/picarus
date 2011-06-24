import heapq
import hadoopy
import os
import cStringIO as StringIO
import Image
import re
import random
from picarus import file_parse
from picarus.report import report_output


def report_categories(hdfs_join_predictions_input, local_output, image_limit, local_thumb_output, **kw):
    # Output a cluster for each category
    # FIXME This is hardcoded for indoor_outdoor, it will have to change when
    # there are multiple classifiers (indoor, outdoor, photos, documents, etc)
    hashes = {-1: [], 1: []}
    totals = {-1: 0, 1: 0}

    # First pass: find images for each category
    for image_hash, (classifier_preds, image_data) in hadoopy.readtb(hdfs_join_predictions_input):
        for classifier, preds in classifier_preds.items():
            posname, negname = classifier.split('_')
            for conf, label in preds:
                totals[label] += 1
                if len(hashes[label]) < image_limit:
                    heapq.heappush(hashes[label], (conf, image_hash))
                else:
                    heapq.heappushpop(hashes[label], (conf, image_hash))

    print negname, len(hashes[-1]), totals[-1]
    print posname, len(hashes[1]), totals[1]

    categories = {}
    categories[posname] = report_output.make_random_clusters([h for _, h in hashes[1]], posname)
    categories[negname] = report_output.make_random_clusters([h for _, h in hashes[-1]], negname)

    try:
        os.makedirs(os.path.dirname(local_output))
    except OSError:
        pass
    file_parse.dump(categories, local_output)

    # Second pass: make image thumbnails
    if local_thumb_output:
        try:
            os.makedirs(local_thumb_output)
        except OSError:
            pass
        hashset = set([h for _, h in hashes[-1] + hashes[1]])
        for image_hash, (classifier_preds, image_data) in hadoopy.readtb(hdfs_join_predictions_input):
            if image_hash in hashset:
                s = StringIO.StringIO()
                s.write(image_data)
                s.seek(0)
                frame = Image.open(s)
                frame.thumbnail((100, 100))
                path = '%s/%s.jpg' % (local_thumb_output, image_hash)
                frame.save(path)


def report_clusters(hdfs_input, local_json_output, sample, category, make_faces, **kw):
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

    try:
        os.makedirs(os.path.dirname(local_json_output))
    except OSError:
        pass
    report = {category: clusters}
    file_parse.dump(report, local_json_output)


def make_thumbnails(hdfs_input, hdfs_output, thumb_size, **kw):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'make_thumbnails.py',
                          reducer=None,
                          cmdenvs=['THUMB_SIZE=%d' % thumb_size])


def report_thumbnails(hdfs_input, hdfs_output, local_thumb_output, thumb_size, **kw):
    """Collect thumbnails of all images in hdfs://${hdfs_input}
    """
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'make_thumbnails.py',
                          reducer=None,
                          cmdenvs=['THUMB_SIZE=%d' % thumb_size])

    try:
        os.makedirs(local_thumb_output)
    except OSError:
        pass
    for image_hash, image_data in hadoopy.readtb(hdfs_output):
        path = '%s/%s.jpg' % (local_thumb_output, image_hash)
        with open(path, 'w') as f:
            f.write(image_data)


def report_video_keyframe(hdfs_input, local_json_output, local_thumb_output, **kw):
    videos = {}
    for (kind, hash), v in hadoopy.readtb(hdfs_input):
        if kind == 'frame' and local_thumb_output is not None:
            s = StringIO.StringIO()
            s.write(v)
            s.seek(0)
            frame = Image.open(s)
            try:
                os.makedirs(local_thumb_output)
            except OSError:
                pass
            frame.save(os.path.join(local_thumb_output, '%s.jpg' % hash))
        if kind == 'video':
            videos[hash] = v

    try:
        os.makedirs(os.path.dirname(local_json_output))
    except OSError:
        pass
    report = {'videos': videos}
    file_parse.dump(report, local_json_output)
