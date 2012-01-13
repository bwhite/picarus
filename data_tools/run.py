import hadoopy
import time

r = 'flickr_data_picarus/run-%f/' % time.time()
tags = 'car person people dog cat table tree flower book desert baseball shoe building sign stallman richard maryland texas'.split()


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def mine_tags(tag_iter, num_iters=1):
    for x, y in enumerate(chunks(tags, 5)):
        hadoopy.writetb(r + 'tags-%.5d/%.5d' % (tag_iter, x), enumerate(y))
    print('Wrote tags')
    metadata_path = r + 'out/flickr_metadata-%.5d' % tag_iter
    hadoopy.launch_frozen(r + 'tags-%.5d' % tag_iter, metadata_path, 'flickr_bulk.py',
                          cmdenvs=['TAG_ITERS=%d' % num_iters])
    return metadata_path

metadata_paths = []
for tag_iter in range(1):
    print('Mined flickr')
    metadata_path = mine_tags(tag_iter)
    metadata_paths.append(metadata_path)
    bulk_tags = sum([x[1]['tags'].split() for x in hadoopy.readtb(metadata_path)], [])
    tag_hist = {}
    for x in bulk_tags:
        try:
            tag_hist[x] += 1
        except KeyError:
            tag_hist[x] = 1
    tags = [y[0] for y in sorted(tag_hist.items(), key=lambda x: x[1], reverse=True)[:100]]
tag_iter += 1
metadata_path = mine_tags(tag_iter, num_iters=5)
metadata_paths.append(metadata_path)
hadoopy.launch_frozen(metadata_paths, r + 'out/flickr_images', 'file_downloader.py')
print('Downloaded images')
