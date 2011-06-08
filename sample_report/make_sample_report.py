import json
import random
import os
import argparse


def videos(vid_jsdir, vid_tdir):
    videojsnames = [x for x in sorted(os.listdir(vid_jsdir))
                    if os.path.splitext(x)[1] == '.js']

    videos = []
    for videojsname in videojsnames:
        with open('%s/%s' % (vid_jsdir, videojsname), 'r') as f:
            videos.append(json.load(f))

    return videos


def random_clusters(imagedir):
    """Creates a test mockup of random clusters from a folder of images
    Returns:
       clusters: a list of clusters that can be JSONified and passed to the
       html renderer
    """
    image_extensions = set(['jpg', 'png', 'jpeg', 'gif', 'ico'])
    local_images = [os.path.splitext(x)[0] for x in sorted(os.listdir(imagedir))
                    if os.path.splitext(x)[1][1:] in image_extensions]

    clusters = []

    n_clusters = max(int(random.normalvariate(6,2)),2)

    # TODO add cluster children to simulate HAC

    for i in range(n_clusters):
        n_images = random.randrange(4,7)
        n_size = random.randrange(40,60)
        cluster = {'all_images': random.sample(local_images, n_size),
                   'sample_images': random.sample(local_images, n_images),
                   'std': random.normalvariate(10.0,2.0),
                   'position': (random.random(), random.random()),
                   'size': n_size,
                   'children': []}
        clusters.append(cluster)
    return clusters


def make_sample_object(imagedir, videosjs, vid_tdir):
    obj = {
        'videos': videos(videosjs, vid_tdir),
        'graphics': random_clusters(imagedir),
        'inappropriate': random_clusters(imagedir),
        'indoor': random_clusters(imagedir),
        'outdoor': random_clusters(imagedir),
        'objects': random_clusters(imagedir),
        }
    return obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve images and features \
    from Cassandra")

    # Thumbnail images
    parser.add_argument('--thumbdir',
                       help='use images from this folder',
                       default='./t/')

    # Videojs folder
    parser.add_argument('--videosjs',
                       help='look for *.js video files in this folder',
                       default='./videojs/')

    # Video thumbnails folder
    parser.add_argument('--vid_tdir',
                       help='thumbnails for video frames',
                       default='./vid_t/')

    # Output js
    parser.add_argument('--outputjs',
                        default='sample_report.js')

    ARGS = parser.parse_args()

    obj = make_sample_object(ARGS.thumbdir,
                             ARGS.videosjs,
                             ARGS.vid_tdir)
    with open(ARGS.outputjs, 'w') as f:
        json.dump(obj, f, indent=2)
