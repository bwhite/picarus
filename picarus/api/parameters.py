# [name]: {module, params}  where params is dict with "name" as key with value {'required': bool, type: (int or float), min, max} with [min, max) or {'required': bool, type: 'bool'} or {'required': enum, vals: [val0, val1, ...]}
PARAM_SCHEMAS = []
PARAM_SCHEMAS.append({'name': 'preprocessor',
                      'type': 'preprocessor',
                      'module': 'imfeat.ImagePreprocessor',
                      'data': 'none',   # none, row, slice
                      'inputs': ['raw_image'],  # abstract columns to be used for input
                      'model_params': {},
                      'module_params': {'compression': {'type': 'enum', 'values': ['jpg']},
                                       'size': {'type': 'int', 'min': 32, 'max': 1025},
                                       'method': {'type': 'enum', 'values': ['force_max_side', 'max_side', 'force_square']}}})

PARAM_SCHEMAS.append({'name': 'histogram',
                      'type': 'feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'imfeat.Histogram',
                      'model_params': {'feature_type': {'type': 'const', 'value': 'feature'}},
                      'module_params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                           'hsv', 'luv', 'hls', 'lab', 'gray']},
                                       'num_bins': {'type': 'int', 'min': 1, 'max': 17},
                                       'style': {'type': 'enum', 'values': ['joint', 'planar']}}})

PARAM_SCHEMAS.append({'name': 'svmlinear',
                      'type': 'classifier',
                      'data': 'slice',
                      'inputs': ['feature', 'meta'],
                      'module': 'sklearn.svm.LinearSVC',
                      'model_params': {'class_positive': {'type': 'str'}, 'classifier_type': {'type': 'const', 'value': 'sklearn_decision_func'}},
                      'module_params': {}})

PARAM_SCHEMAS.append({'name': 'rrmedian',
                      'type': 'hasher',
                      'data': 'slice',
                      'inputs': ['feature'],
                      'module': 'image_search.RRMedianHasher',
                      'model_params': {},
                      'module_params': {'hash_bits': {'type': 'int', 'min': 1, 'max': 513}, 'normalize_features': {'type': 'const', 'value': False}}})


PARAM_SCHEMAS.append({'name': 'linear',
                      'type': 'index',
                      'data': 'slice',
                      'inputs': ['hash', 'meta'],
                      'module': 'image_search.LinearHashDB',
                      'model_params': {},
                      'module_params': {}})


PARAM_SCHEMAS.append({'name': 'imageblocks',
                      'type': 'multi_feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'picarus.modules.ImageBlocks',
                      'model_params': {'feature_type': {'type': 'const', 'value': 'multi_feature'}},
                      'module_params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                            'hsv', 'luv', 'hls', 'lab', 'gray']},
                                        'num_sizes': {'type': 'int', 'min': 1, 'max': 5},
                                        'sbin': {'type': 'int', 'min': 8, 'max': 257}}})

PARAM_SCHEMAS.append({'name': 'nbnnlocal',
                      'type': 'classifier',
                      'data': 'slice',
                      'inputs': ['multi_feature', 'meta'],
                      'module': 'picarus.modules.LocalNBNNClassifier',
                      'model_params': {'classifier_type': {'type': 'const', 'value': 'class_distance_list'}},
                      'module_params': {}})


PARAM_SCHEMAS_SERVE = {}

for x in PARAM_SCHEMAS:
    schema = dict(x)
    schema['prefix'] = {'feature': 'feat:', 'preprocessor': 'data:', 'classifier': 'pred:', 'hasher': 'hash:', 'index': 'srch:', 'multi_feature': 'mfeat:'}[x['type']]
    PARAM_SCHEMAS_SERVE['/'.join([x['type'], x['name']])] = schema
