import imfeat
import distpy
import hadoopy
import numpy as np
import cv2
import cPickle as pickle


def compute_feature(image):
    return compute_features([image]).next()

def compute_features(images):
    #feat = imfeat.GIST()
    feat = imfeat.Histogram('lab', num_bins=8)
    for image in images:
        yield feat(imfeat.resize_image(image, 256, 256))

def compute_hash(feature, median_feature):
    feature = feature.reshape((1, feature.size))
    return compute_hashes(feature, median_feature).ravel()

def compute_hashes(features, median_feature):
    bit_shape = (features.shape[0], int(np.ceil(features.shape[1] / 8.)))
    return np.packbits(np.array(features > median_feature, dtype=np.uint8)).reshape(bit_shape)


def load_data(max_images=1000):
    images = []
    image_metadatas = []
    for url, (image_data, image_metadata) in hadoopy.readtb('/user/brandyn/flickr_data/run-1325960005.138596/out/flickr_join2'):
        print(url)
        if len(images) >= max_images:
            break
        images.append(imfeat.image_fromstring(image_data, {'type': 'numpy', 'dtype': 'uint8', 'mode': 'bgr'}))
        image_metadata['tags'] = image_metadata['tags'].split()
        image_metadatas.append(image_metadata)
    return images, image_metadatas


def compute_database():
    images, image_metadatas = load_data()
    features = np.array(list(compute_features(images)))
    median_feature = np.median(features, 0)
    hashes = compute_hashes(features, median_feature)
    return hashes, image_metadatas, median_feature


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
    
    # load test image
    image = cv2.imread('target.jpg')
    print(evaluate_image(image, hashes, image_metadatas, median_feature))

main()
