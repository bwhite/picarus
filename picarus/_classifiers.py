import classipy
import pyram
import cPickle as pickle
import hadoopy


def train(classifier_name, classifier_extra, label_values):
    label_values = list(label_values)
    hadoopy.counter('FeatureShape', str(len(label_values[0][1])))
    if classifier_name == 'svmlinear':
        return classipy.SVMLinear(options={'B': '1'}).train(label_values)
    elif classifier_name == 'svm':
        return classipy.SVM(options={'t': '2'}).train(label_values)
    elif classifier_name == 'svm_hik':
        return classipy.SVMScikit(kernel=classipy.kernels.histogram_intersection)
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
    return pickle.dumps({'classifier_name': classifier_name,
                         'classifier_extra': classifier_extra,
                         'classifier': classifier.dumps()})


def loads(classifier_ser):
    d = pickle.loads(classifier_ser)
    if d['classifier_name'] in ('svmlinear', 'svmlinear_autotune'):
        return classipy.SVMLinear.loads(d['classifier'])
    elif d['classifier_name'] == 'svm':
        return classipy.SVM.loads(d['classifier'])
    elif d['classifier_name'] == 'svm_hik':
        return classipy.SVMScikit.loads(d['classifier'])
    else:
        raise ValueError('Unknown classifier [%s]' % d['classifier_name'])
