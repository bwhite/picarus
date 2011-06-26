import classipy
import cPickle as pickle


def train(classifier_name, classifier_extra, label_values):
    if classifier_name == 'svmlinear':
        return classipy.SVMLinear(options={'B': '1'}).train(label_values)
    elif classifier_name == 'svm':
        return classipy.SVM(options={'t': '2'}).train(label_values)
    else:
        raise ValueError('Unknown classifier [%s]' % classifier_name)


def dumps(classifier_name, classifier_extra, classifier):
    return pickle.dumps({'classifier_name': classifier_name,
                         'classifier_extra': classifier_extra,
                         'classifier': classifier.dumps()})


def loads(classifier_ser):
    d = pickle.loads(classifier_ser)
    if d['classifier_name'] == 'svmlinear':
        return classipy.SVMLinear.loads(d['classifier'])
    elif d['classifier_name'] == 'svm':
        return classipy.SVM.loads(d['classifier'])
    else:
        raise ValueError('Unknown classifier [%s]' % d['classifier_name'])
