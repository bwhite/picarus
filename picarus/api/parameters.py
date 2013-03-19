# [name]: {module, params}  where params is dict with "name" as key with value {'required': bool, type: (int or float), min, max} with [min, max) or {'required': bool, type: 'bool'} or {'required': enum, vals: [val0, val1, ...]}
PARAM_SCHEMAS = []
PARAM_SCHEMAS.append({'name': 'preprocessor',
                      'output_type': 'processed_image',
                      'module': 'picarus.ImagePreprocessor',
                      'data': 'none',   # none, row, slice
                      'inputs': ['raw_image'],  # abstract columns to be used for input
                      'model_params': {},
                      'module_params': {'compression': {'type': 'enum', 'values': ['jpg']},
                                        'size': {'type': 'int', 'min': 32, 'max': 1025},
                                        'method': {'type': 'enum', 'values': ['force_max_side', 'max_side', 'force_square']}}})

PARAM_SCHEMAS.append({'name': 'histogram',
                      'output_type': 'feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'picarus.HistogramImageFeature',
                      'model_params': {},
                      'module_params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                            'hsv', 'luv', 'hls', 'lab']},
                                        'num_bins': {'type': 'int', 'min': 1, 'max': 17},
                                        'levels': {'type': 'int', 'min': 1, 'max': 3}}})


PARAM_SCHEMAS.append({'name': 'svmlinear',
                      'output_type': 'binary_class_confidence',
                      'data': 'slice',
                      'inputs': ['feature', 'meta'],
                      'module': 'sklearn.svm.LinearSVC',
                      'model_params': {'class_positive': {'type': 'str'}},
                      'module_params': {}})

PARAM_SCHEMAS.append({'name': 'rrmedian',
                      'output_type': 'hash',
                      'data': 'slice',
                      'inputs': ['feature'],
                      'module': 'image_search.RRMedianHasher',
                      'model_params': {},
                      'module_params': {'hash_bits': {'type': 'int', 'min': 1, 'max': 513}, 'normalize_features': {'type': 'const', 'value': False}}})


# TODO: need to update this, think about what output_type should be
#PARAM_SCHEMAS.append({'name': 'linear',
#                      'output_type': 'index',
#                      'data': 'slice',
#                      'inputs': ['hash', 'meta'],
#                      'module': 'image_search.LinearHashDB',
#                      'model_params': {},
#                      'module_params': {}})


PARAM_SCHEMAS.append({'name': 'imageblocks',
                      'output_type': 'multi_feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'picarus.modules.ImageBlocks',
                      'model_params': {},
                      'module_params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                            'hsv', 'luv', 'hls', 'lab', 'gray']},
                                        'num_sizes': {'type': 'int', 'min': 1, 'max': 5},
                                        'sbin': {'type': 'int', 'min': 8, 'max': 257}}})

PARAM_SCHEMAS.append({'name': 'nbnnlocal',
                      'output_type': 'multi_class_distance',
                      'data': 'slice',
                      'inputs': ['multi_feature', 'meta'],
                      'module': 'picarus.modules.LocalNBNNClassifier',
                      'model_params': {},
                      'module_params': {}})


PARAM_SCHEMAS_SERVE = {}

for x in PARAM_SCHEMAS:
    schema = dict(x)
    schema['prefix'] = {'feature': 'feat:', 'processed_image': 'data:', 'binary_class_confidence': 'pred:', 'multi_class_distance': 'pred:', 'hash': 'hash:', 'index': 'srch:', 'multi_feature': 'mfeat:'}[x['output_type']]
    PARAM_SCHEMAS_SERVE['/'.join([x['output_type'], x['name']])] = schema
