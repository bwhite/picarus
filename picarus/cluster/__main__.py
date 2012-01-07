import hadoopy
import os
import tempfile
import numpy as np
import cPickle as pickle
import picarus
import scipy as sp


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def _parser(sps):
    import picarus.__main__
    ca = picarus.__main__._ca
    # Whiten Features
    s = sps.add_parser('whiten', help='Scale features to zero mean unit variance')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('hdfs_output', **ca['output'])
    s.set_defaults(func=picarus.cluster.run_whiten)

    # Uniform Sample
    s = sps.add_parser('sample', help='Uniformly sample a specified number of features (random clustering)')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('num_clusters', **ca['num_clusters'])
    s.add_argument('--local_json_output', help='Local output path')  # TODO: Implement
    s.set_defaults(func=picarus.cluster.run_sample)

    # K-Means Cluster
    s = sps.add_parser('kmeans', help='K-Means Cluster')
    s.add_argument('hdfs_input', **ca['input'])
    s.add_argument('hdfs_prev_clusters', help='HDFS path to previous clusters')
    s.add_argument('hdfs_image_data', **ca['image_data'])
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('num_clusters', **ca['num_clusters'])
    s.add_argument('num_iters', type=int, help='Maximum number of iterations')
    s.add_argument('num_samples', type=int, help='Number of samples')
    s.add_argument('--local_json_output', help='Local output path')
    s.set_defaults(func=picarus.cluster.run_kmeans)


def run_whiten(hdfs_input, hdfs_output, image_hashes=None, **kw):
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf('whiten.py'),
                           image_hashes=image_hashes)


def run_sample(hdfs_input, hdfs_output, num_clusters, **kw):
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf('random_sample.py'),
                          cmdenvs=['SAMPLE_SIZE=%d' % num_clusters])


def _run_local_kmeans(data, q, num_clusters):
    import scipy.cluster
    print('Starting to cluster')
    clusters = sp.cluster.vq.kmeans(data, num_clusters)[0]
    print('Putting clusters')
    while 1:
        try:
            q.put(clusters, timeout=10)
            break
        except Queue.Full:
            print('Queue put failed')
            time.sleep(0)
    print('Done Putting clusters')


def run_local_kmeans(hdfs_input, hdfs_output, num_clusters, *args, **kw):
    import multiprocessing
    import Queue
    import time
    q = multiprocessing.Queue()
    data = np.asfarray([y for x, y in hadoopy.readtb(hdfs_input)])
    p = multiprocessing.Process(target=_run_local_kmeans, args=(data, q, num_clusters))
    p.start()
    while 1:
        try:
            clusters = q.get(timeout=10)
            break
        except Queue.Empty:
            print('Queue get failed')
            time.sleep(0)
    p.join()
    hadoopy.writetb(hdfs_output, enumerate(clusters))
    print('Done Writing to HDFS')
    print('Done joining')


def run_kmeans(hdfs_input, hdfs_prev_clusters, hdfs_image_data, hdfs_output, num_clusters,
               num_iters, num_samples, metric='l2sqr', local_json_output=None, image_hashes=None, **kw):
    for cur_iter_num in range(num_iters):
        clusters_fp = fetch_clusters_from_hdfs(hdfs_prev_clusters)
        clusters_fn = os.path.basename(clusters_fp.name)
        cur_output = '%s/clust%.6d' % (hdfs_output, cur_iter_num)
        picarus._launch_frozen(hdfs_input, cur_output, _lf('kmeans.py'),
                               cmdenvs=['CLUSTERS_FN=%s' % clusters_fn],
                               files=[clusters_fp.name],
                               num_reducers=max(1, num_clusters / 2),
                               dummy_arg=clusters_fp)
        hdfs_prev_clusters = cur_output
    print('Clusters[%s]' % hdfs_prev_clusters)
    # Compute K-Means assignment/samples
    clusters_fp = fetch_clusters_from_hdfs(hdfs_prev_clusters)
    clusters_fn = os.path.basename(clusters_fp.name)
    cur_output = '%s/partition' % hdfs_output
    picarus._launch_frozen([hdfs_input, hdfs_image_data], cur_output, _lf('kmeans_partition.py'),
                           cmdenvs=['CLUSTERS_FN=%s' % clusters_fn],
                           files=[clusters_fp.name],
                           num_reducers=max(1, num_clusters / 2),
                           image_hashes=image_hashes,
                           dummy_arg=clusters_fp)
    cur_output = '%s/assign' % hdfs_output
    picarus._launch_frozen(hdfs_input, cur_output, _lf('kmeans_assign.py'),
                          cmdenvs=['CLUSTERS_FN=%s' % clusters_fn,
                                   'NUM_SAMPLES=%d' % num_samples,
                                   'mapred.text.key.partitioner.options=-k1'],
                          files=[clusters_fp.name],
                          num_reducers=max(1, num_clusters / 2),
                          partitioner='org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner',
                          dummy_arg=clusters_fp)
    print('Assignment[%s]' % cur_output)
    # Filter the samples
    assignments_fp = fetch_assignments_from_hdfs(cur_output)
    assignments_fn = os.path.basename(assignments_fp.name)
    cur_output = '%s/samples' % hdfs_output
    picarus._launch_frozen(hdfs_image_data, cur_output, _lf('filter_samples.py'),
                          cmdenvs=['ASSIGNMENTS_FN=%s' % os.path.basename(assignments_fn)],
                          files=[assignments_fp.name],
                          reducer=None,
                          dummy_arg=assignments_fp)
    print('Samples[%s]' % cur_output)


def run_hac(hdfs_input, **kw):
    import scipy as sp
    import scipy.cluster
    import scipy.spatial.distance
    x = np.array([x[1] for x in hadoopy.readtb(hdfs_input)])
    y = sp.spatial.distance.pdist(x)
    return sp.cluster.hierarchy.linkage(y)
    


def fetch_clusters_from_hdfs(hdfs_input):
    """Fetch remote clusters and store locally

    Clusters are sorted to allow comparing between iterations

    Args:
        hdfs_input: HDFS input path

    Returns:
        NamedTemporaryFile holding the cluster data
    """
    clusters_fp = tempfile.NamedTemporaryFile()
    clusters = [v.tolist() for k, v in hadoopy.readtb(hdfs_input)]
    clusters.sort()
    clusters = np.ascontiguousarray(clusters, dtype=np.float64)
    pickle.dump(clusters, clusters_fp, -1)
    clusters_fp.seek(0)
    return clusters_fp


def fetch_assignments_from_hdfs(hdfs_input):
    """Fetch remote assignments and store locally

    Args:
        hdfs_input: HDFS input path

    Returns:
        NamedTemporaryFile holding the assignment data
    """
    assignments_fp = tempfile.NamedTemporaryFile()
    assignments = list(hadoopy.readtb(hdfs_input))
    pickle.dump(assignments, assignments_fp, -1)
    assignments_fp.seek(0)
    return assignments_fp
