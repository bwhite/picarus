import classipy
import pyram
import cPickle as pickle
import hadoopy
import zlib


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
    else:
        raise ValueError('Unknown classifier [%s]' % classifier_name)


def dumps(classifier_name, classifier_extra, classifier):
    if classifier_name in ['svm_hik']:
        return pickle.dumps({'classifier_name': classifier_name,
                             'classifier_extra': classifier_extra,
                             'classifier': zlib.compress(classifier.dumps())})
    return pickle.dumps({'classifier_name': classifier_name,
                         'classifier_extra': classifier_extra,
                         'classifier': classifier.dumps()})


def loads(classifier_ser):
    d = pickle.loads(classifier_ser)
    classifier_name = d['classifier_name']
    if classifier_name in ('svmlinear', 'svmlinear_autotune'):
        return classipy.SVMLinear.loads(d['classifier'])
    elif classifier_name == 'svm':
        return classipy.SVM.loads(d['classifier'])
    elif classifier_name == 'svm_hik':
        import sys
        decomp = zlib.decompress(d['classifier'])
        del d  # NOTE(brandyn): Some of these get very large
        sys.stderr.write('[%s] DecompSz[%d]\n' % (classifier_name, len(decomp)))
        return classipy.SVMScikit.loads(decomp)
    else:
        raise ValueError('Unknown classifier [%s]' % classifier_name)
