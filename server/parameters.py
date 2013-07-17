# [name]: {module, params}  where params is dict with "name" as key with value {'required': bool, type: (int or float), min, max} with [min, max) or {'required': bool, type: 'bool'} or {'required': enum, vals: [val0, val1, ...]}

# Factory
# type: factory
# path:
# kind: classifier, feature, preprocessor, hasher, index
# input_types:
# data: Slice/Slices/Row
# params:


# Model
# type: model
# module:
# kind: classifier, feature, preprocessor, hasher, index
# input_type:
# output_type:
# params:

import sys

PARAM_SCHEMAS = []
PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.ImagePreprocessor',
                      'kind': 'image_preprocessor',
                      'input_type': 'raw_image',
                      'output_type': 'processed_image',
                      'params': {'compression': {'type': 'enum', 'values': ['jpg', 'png', 'ppm']},
                                 'size': {'type': 'int', 'min': 16, 'max': 1025},
                                 'method': {'type': 'enum', 'values': ['force_max_side', 'max_side', 'force_square']}}})

PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.ImageWarp',
                      'kind': 'image_preprocessor',
                      'input_type': 'raw_image',
                      'output_type': 'processed_image',
                      'params': {'compression': {'type': 'enum', 'values': ['jpg', 'png', 'ppm']},
                                 'h': {'type': 'float_list', 'min': -9007199254740992., 'max': 9007199254740992, 'min_size': 9, 'max_size': 10},
                                 'height': {'type': 'int', 'min': 1, 'max': 1025},
                                 'width': {'type': 'int', 'min': 1, 'max': 1025}}})


PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.HistogramImageFeature',
                      'kind': 'feature',
                      'input_type': 'processed_image',
                      'output_type': 'feature',
                      'params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                     'hsv', 'luv', 'hls', 'lab']},
                                 'num_bins': {'type': 'int_list', 'min': 1, 'max': 17, 'min_size': 3, 'max_size': 4},
                                 'levels': {'type': 'int', 'min': 1, 'max': 3}}})

PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.GISTImageFeature',
                      'kind': 'feature',
                      'input_type': 'processed_image',
                      'output_type': 'feature',
                      'params': {'orientations_per_scale': {'type': 'int_list', 'min': 1, 'max': 9, 'min_size': 1, 'max_size': 4},
                                 'num_blocks': {'type': 'int', 'min': 1, 'max': 8}}})


PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.PixelsImageFeature',
                      'kind': 'feature',
                      'input_type': 'processed_image',
                      'output_type': 'feature',
                      'params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                     'hsv', 'luv', 'hls', 'lab']}}})


PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.HOGImageMaskFeature',
                      'kind': 'feature',
                      'input_type': 'processed_image',
                      'output_type': 'mask_feature',
                      'params': {'bin_size': {'type': 'int', 'min': 2, 'max': 65}}})


PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.BinaryPredictor',
                      'kind': 'classifier',
                      'input_type': 'binary_class_confidence',
                      'output_type': 'binary_prediction',
                      'params': {'threshold': {'type': 'float', 'min': -sys.float_info.max, 'max': sys.float_info.max}}})

PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.BRISKImageFeature2d',
                      'kind': 'feature2d',
                      'input_type': 'processed_image',
                      'output_type': 'feature2d_binary',
                      'params': {'thresh': {'type': 'int', 'min': 1, 'max': 256},
                                 'octaves': {'type': 'int', 'min': 1, 'max': 6},
                                 'pattern_scale': {'type': 'float', 'min': .1, 'max': 10.}}})


PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.FREAKImageFeature2d',
                      'kind': 'feature2d',
                      'input_type': 'processed_image',
                      'output_type': 'feature2d_binary',
                      'params': {'thresh': {'type': 'int', 'min': 1, 'max': 256},
                                 'orientation_norm': {'type': 'bool'},
                                 'scale_norm': {'type': 'bool'},
                                 'octaves': {'type': 'int', 'min': 1, 'max': 6},
                                 'pattern_scale': {'type': 'float', 'min': .1, 'max': 32.}}})


PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.FaceImageObjectDetector',
                      'kind': 'detector',
                      'input_type': 'processed_image',
                      'output_type': 'image_detections',
                      'params': {'scale_factor': {'type': 'float', 'min': 1, 'max': 10},
                                 'min_neighbors': {'type': 'int', 'min': 0, 'max': 10},
                                 'min_size': {'type': 'int', 'min': 0, 'max': 1025},
                                 'max_size': {'type': 'int', 'min': 0, 'max': 1025}}})


PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.BlocksImageMultiFeature',
                      'kind': 'feature',
                      'input_type': 'processed_image',
                      'output_type': 'multi_feature',
                      'params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                     'hsv', 'luv', 'hls', 'lab']},
                                 'levels': {'type': 'int', 'min': 1, 'max': 5},
                                 'block_size': {'type': 'int', 'min': 16, 'max': 129}}})

PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'svmlinear',
                      'kind': 'classifier',
                      'data': 'slices',
                      'input_types': ['feature', 'meta'],
                      'params': {'class_positive': {'type': 'str'}}})


PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'svmkernel',
                      'kind': 'classifier',
                      'data': 'slices',
                      'input_types': ['feature', 'meta'],
                      'params': {'class_positive': {'type': 'str'},
                                 'kernel': {'type': 'enum', 'values': ['hik']}}})


PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'bovw',
                      'kind': 'feature',
                      'data': 'slices',
                      'input_types': ['mask_feature'],
                      'params': {'max_samples': {'type': 'int', 'min': 1000, 'max': 50000},
                                 'num_clusters': {'type': 'int', 'min': 2, 'max': 1000},
                                 'levels': {'type': 'int', 'min': 1, 'max': 4}}})

PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'spherical',
                      'kind': 'hasher',
                      'data': 'slices',
                      'input_types': ['feature'],
                      'params': {'num_pivots': {'type': 'int', 'min': 1, 'max': 513},
                                 'eps_m': {'type': 'float', 'min': 0., 'max': 1.},
                                 'eps_s': {'type': 'float', 'min': 0., 'max': 1.},
                                 'max_iters': {'type': 'int', 'min': 1, 'max': 101}}})

PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'spherical',
                      'kind': 'index',
                      'data': 'slices',
                      'input_types': ['hash'],
                      'params': {'max_results': {'type': 'int', 'min': 1, 'max': 101}}})


PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'hamming_feature_2d',
                      'kind': 'index',
                      'data': 'slices',
                      'input_types': ['feature2d_binary'],
                      'params': {'max_results': {'type': 'int', 'min': 1, 'max': 101},
                                 'max_keypoint_results': {'type': 'int', 'min': 1, 'max': 1025},
                                 'hamming_thresh': {'type': 'int', 'min': 1, 'max': 266}}})

PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'localnbnn',
                      'kind': 'classifier',
                      'data': 'slices',
                      'input_types': ['multi_feature', 'meta'],
                      'params': {'max_results': {'type': 'int', 'min': 1, 'max': 64}}})




PARAM_SCHEMAS_SERVE = {}


for x in PARAM_SCHEMAS:
    schema = dict(x)
    PARAM_SCHEMAS_SERVE['/'.join([x['type'], x['kind'], x['name']])] = schema
