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

PARAM_SCHEMAS = []
PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.ImagePreprocessor',
                      'kind': 'image_preprocessor',
                      'input_type': 'raw_image',
                      'output_type': 'processed_image',
                      'params': {'compression': {'type': 'enum', 'values': ['jpg']},
                                 'size': {'type': 'int', 'min': 32, 'max': 1025},
                                 'method': {'type': 'enum', 'values': ['force_max_side', 'max_side', 'force_square']}}})

PARAM_SCHEMAS.append({'type': 'model',
                      'name': 'picarus.HistogramImageFeature',
                      'kind': 'feature',
                      'input_type': 'processed_image',
                      'output_type': 'feature',
                      'params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                     'hsv', 'luv', 'hls', 'lab']},
                                 'num_bins': {'type': 'int', 'min': 1, 'max': 17},
                                 'levels': {'type': 'int', 'min': 1, 'max': 3}}})

#PARAM_SCHEMAS.append({'type': 'model',
#                      'name': 'picarus.modules.ImageBlocks',
#                      'kind': 'feature',
#                      'input_type': 'processed_image',
#                      'output_type': 'multi_feature',
#                      'params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
#                                                                     'hsv', 'luv', 'hls', 'lab', 'gray']},
#                                 'num_sizes': {'type': 'int', 'min': 1, 'max': 5},
#                                 'sbin': {'type': 'int', 'min': 8, 'max': 257}}})

PARAM_SCHEMAS.append({'type': 'factory',
                      'name': 'svmlinear',
                      'kind': 'classifier',
                      'data': 'slices',
                      'input_types': ['feature', 'meta'],
                      'params': {'class_positive': {'type': 'str'}}})

#PARAM_SCHEMAS.append({'type': 'factory',
#                      'name': 'nbnnlocal',
#                      'kind': 'classifier',
#                      'data': 'slices',
#                      'input_types': ['multi_feature', 'meta'],
#                      'params': {}})


#PARAM_SCHEMAS.append({'type': 'factory',
#                      'name': 'rrmedian',
#                      'kind': 'hasher',
#                      'data': 'slices',
#                      'input_types': ['feature'],
#                      'params': {'hash_bits': {'type': 'int', 'min': 1, 'max': 513}, 'normalize_features': {'type': 'const', 'value': False}}})


# TODO: need to update this, think about what output_type should be
#PARAM_SCHEMAS.append({'type': 'factory',
#                      'path': 'linear',
#                      'kind': 'index',
#                      'data': 'slices',
#                      'input_types': ['hash', 'meta'],
#                      'params': {}})



PARAM_SCHEMAS_SERVE = {}


for x in PARAM_SCHEMAS:
    schema = dict(x)
    PARAM_SCHEMAS_SERVE['/'.join([x['type'], x['kind'], x['name']])] = schema
