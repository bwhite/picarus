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


