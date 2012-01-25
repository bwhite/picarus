from build_database import compute_database, compute_hash, compute_feature
import imfeat
import distpy
import hadoopy
import numpy as np
import cv2
import cPickle as pickle

def evaluate_image(image, hashes, image_metadatas, median_feature, k=50, max_tags=10):
    h = compute_hash(compute_feature(image), median_feature)
    # Compute K-nn
    d = distpy.Hamming(len(h))
    tags = []
    with open('results.html', 'w') as fp:
        fp.write('<img height=250 src=%s \><br>' % 'target.jpg')
        for distance, index in d.knn(hashes, h, k):  # (distance, index) (k x 2)
            tags += image_metadatas[index]['tags']
            fp.write('<img height=150 src=%s \>' % image_metadatas[index]['url_m'])
    # Pool tags
    tag_hist = {}
    for tag in tags:
        try:
            tag_hist[tag] += 1
        except KeyError:
            tag_hist[tag] = 1
    return sorted(tag_hist.items(), reverse=True, key=lambda x: x[1])[:max_tags]


def main():
    try:
        with open('database.pkl') as fp:
            hashes, image_metadatas, median_feature = pickle.load(fp)
    except IOError:
        hashes, image_metadatas, median_feature = compute_database()
        with open('database.pkl', 'w') as fp:
            pickle.dump((hashes, image_metadatas, median_feature), fp, -1)
    hashes = np.array([x.ravel() for x in hashes])
    for x in image_metadatas:
        x['tags'] = x['tags'].split()
    print(hashes.shape)
    print('Model loaded')
    # load test image
    image = cv2.imread('target.jpg')
    print(evaluate_image(image, hashes, image_metadatas, median_feature))

main()
