import numpy as np
import matplotlib.pyplot as mp


def confusion_matrix(true_preds, N):
    conf_mat = np.zeros((N, N))
    for true_class, pred_class in true_preds:
        conf_mat[true_class][pred_class] += 1
    return conf_mat


def save_confusion_matrix(conf_mat, classes, filename='confmat.png', title='Confusion matrix'):
    N = len(classes)
    conf_mat = np.asfarray(conf_mat)
    assert N == conf_mat.shape[0] == conf_mat.shape[1]
    conf_mat /= np.sum(conf_mat)

    # draw the confusion matrix
    fig = mp.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_yticks(np.arange(N))
    ax.set_yticklabels([classes[i] for i in range(N)])
    ax.set_xticks(np.arange(N))
    ax.set_xticklabels([classes[i] for i in range(N)], rotation='vertical')
    res = ax.imshow(np.array(conf_mat), interpolation='nearest')
    fig.colorbar(res)
    for i, cas in enumerate(conf_mat):
        for j, c in enumerate(cas):
            if c>0:
                mp.text(j-.2, i+.2, int(round(c * 100)), fontsize=12)
    mp.title(title)
    mp.savefig(filename, format="png")


def demo():
    classes = ['turtle', 'fish', 'lobster']
    true_preds = [(np.random.randint(0, 3), np.random.randint(0, 3)) for x in range(100)]
    save_confusion_matrix(confusion_matrix(true_preds, 3), classes)


if __name__ == '__main__':
    demo()
