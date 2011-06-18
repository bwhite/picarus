import random


def make_image(imagehash, category, make_faces=False):
    if not make_faces:
        faces = []
    else:
        num_faces = random.randint(1,2)

        def make_face():
            w,h = random.random()/3+.1, random.random()/3+.1
            x,y = random.random()/3+.5, random.random()/3+.5
            return ((x-w/2,y-h/2), (x+w/2,y+h/2))
        faces = [make_face() for _ in range(num_faces)]

    return {
        'hash': imagehash,
        'categories': [category],
        'video': [],
        'faces': faces,
        }


def make_random_clusters(image_hashes, category):
    """Make a bunch of clusters from a category of images
    """
    local_images = [make_image(h, category) for h in image_hashes]
    n_clusters = 1  # random.randrange(8,10)
    clusters = []
    for i in range(n_clusters):
        n_images = min(len(local_images), random.randrange(300,301))
        n_size = min(len(local_images), random.randrange(300,301))
        cluster = {'all_images': random.sample(local_images, n_size),
                   'sample_images': random.sample(local_images, n_images),
                   'std': random.normalvariate(10.0,2.0),
                   'position': (random.random(), random.random()),
                   'size': n_size,
                   'children': []}
        clusters.append(cluster)
    return clusters
