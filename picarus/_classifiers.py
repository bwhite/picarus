import classipy
import pyram
import cPickle as pickle
import hadoopy
import zlib
import sklearn.svm
import sklearn.pls
import sklearn.metrics
import sklearn.cross_validation
import sklearn.grid_search
import sklearn.pipeline
import numpy as np
import snappy


def train(classifier_name, classifier_extra, label_values):
    label_values = list(label_values)
    hadoopy.counter('FeatureShape', str(len(label_values[0][1])))
    if classifier_name == 'svmlinear':
        return classipy.SVMLinear(options={'B': '1'}).train(label_values)
    elif classifier_name == 'svm':
        return classipy.SVM(options={'t': '2'}).train(label_values)
    elif classifier_name == 'svm_hik':
        return classipy.SVMScikit(kernel=classipy.kernels.histogram_intersection).train(label_values)
    elif classifier_name == 'svmlinear_autotune':

        def wrapped_optimizer(*args, **kw):
            for x in pyram.exponential_grid(*args, **kw):
                hadoopy.counter('X-Val', 'Rounds')
                yield x
        b = classipy.select_parameters(classipy.SVMLinear, label_values,
                                       {'c': (10**-2, 10**1, 10)},
                                       wrapped_optimizer,
                                       options={'B': '1'})[1]
        print(b)
        return classipy.SVMLinear(b).train(label_values)
    elif classifier_name == 'plslinearsvmxval':
        num_dims = label_values[0][1].size
        # Set the parameters by cross-validation
        #,'pls__n_components': [x for x in [1, 8, 16, 32, 64, 128, 256] if x <= num_dims]
        #('pls', sklearn.pls.PLSRegression(n_components=0)),
        tuned_parameters = [{'svm__C': [.001, .01, .1, 1, 10, 100]}]
        p = sklearn.pipeline.Pipeline([('svm', sklearn.svm.SVC(kernel=classipy.kernels.histogram_intersection, scale_C=True))])  # was cls
        #p = sklearn.grid_search.GridSearchCV(cls, tuned_parameters, score_func=sklearn.metrics.f1_score)
        num_neg = 0
        num_pos = 0
        import random
        random.shuffle(label_values)
        new_label_values = []
        for l, v in label_values:
            if l == 1:
                if num_pos < 100:
                    new_label_values.append((l, v))
                num_pos += 1
            else:
                if num_neg < 100:
                    new_label_values.append((l, v))
                num_neg += 1
        import sys
        sys.stderr.write('Num Neg[%d] Pos[%d]\n' % (num_neg, num_pos))
        p.fit(*zip(*new_label_values)[::-1])
        return p  # p.best_estimator_
    else:
        raise ValueError('Unknown classifier [%s]' % classifier_name)


def dumps(classifier_name, classifier_extra, classifier):
    return snappy.compress(pickle.dumps({'classifier_name': classifier_name,
                                         'classifier_extra': classifier_extra,
                                         'classifier': classifier}, -1))


def loads(classifier_ser):
    d = pickle.loads(snappy.decompress(classifier_ser))
    if d['classifier_name'] == 'plslinearsvmxval':
        def decision_function(x):
            for step_name, step in d['classifier'].steps[:-1]:
                x = step.transform(x)
            return d['classifier'].steps[-1][1].decision_function(x)
        d['classifier'].decision_function = decision_function
    return d['classifier']
