import numpy as np
import random


def _pivot_dist(points, pivot):
    points_diff = points - pivot
    points_diff *= points_diff
    return np.sum(points_diff, 1)


def _compute_thresholds(points, pivots):
    median_ind = len(points) / 2
    threshs = np.zeros(pivots.shape[0])
    for i, pivot in enumerate(pivots):
        dists = _pivot_dist(points, pivot)
        dists.sort()
        threshs[i] = dists[median_ind]
    return threshs


def _compute_pivot_memberships(points, pivots, threshs):
    assert pivots.shape[0] == threshs.size
    assert pivots.shape[1] == points.shape[1]
    memberships = np.zeros((pivots.shape[0], points.shape[0]), dtype=np.bool)
    for i, (t, pivot) in enumerate(zip(threshs, pivots)):
        memberships[i, :] = _pivot_dist(points, pivot) >= t
    return memberships


def _compute_pivot_cooccurrences(memberships):
    o = np.zeros((memberships.shape[0], memberships.shape[0]))
    for i in range(memberships.shape[0]):
        memberships_i = memberships[:, memberships[i, :].nonzero()[0]]
        o[i, :] = np.sum(memberships_i, 1)  # NOTE(brandyn): This can be sped up by 2x, triangle
    return o


def _update_pivots(pivots, o, m_div_4):
    f = np.zeros((pivots.shape[0], pivots.shape[0], pivots.shape[1]))
    for i in range(pivots.shape[0] - 1):
        for j in range(i + 1, pivots.shape[0]):
            f[i, j, :] = (pivots[i] - pivots[j]) * (o[i, j] - m_div_4) / (m_div_4 * 2)
            f[j, i, :] = -f[i, j, :]
    for i, pivot in enumerate(pivots):
        pivot += np.mean(f[i, :, :], 0)


def train(points, num_pivots, eps_m, eps_s, max_iters):
    num_pivots = min(points.shape[0], num_pivots)
    #pivots = np.asfarray(random.sample(points, num_pivots))
    pivots = np.asfarray(points[:num_pivots, :]).copy()
    m_div_4 = points.shape[0] / 4.
    for x in range(max_iters):
        for x in pivots.tolist()[:1]:
            print(' '.join('%.6f' % y for y in x[:5]))
        threshs = _compute_thresholds(points, pivots)
        memberships = _compute_pivot_memberships(points, pivots, threshs)
        o = _compute_pivot_cooccurrences(memberships)
        triu = np.triu_indices(num_pivots, 1)
        mean_ratio = np.mean(np.abs(o[triu] - m_div_4)) / (m_div_4 * eps_m)
        var_ratio = np.var(o[triu]) / (eps_s * m_div_4) ** 2
        print((mean_ratio, var_ratio))
        if mean_ratio <= 1. and var_ratio <= 1:
            break
        _update_pivots(pivots, o, m_div_4)
    return {'pivots': pivots, 'threshs': threshs}


def train_takeout(*args, **kw):
    out = train(*args, **kw)
    return {'pivots': out['pivots'].ravel().tolist(),
            'threshs': out['threshs'].tolist()}
