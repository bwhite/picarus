import hadoopy
import time

r = 'flickr_data/run-%f/' % time.time()
tags = 'christmas flower rose bird tree'
for x, y in enumerate(tags.split()):
    hadoopy.writetb(r + 'tags/%.4d' % x, [(0, y)])
print('Wrote tags')
hadoopy.launch_frozen(r + 'tags', r + 'out/flickr_metadata', 'flickr_bulk.py')
print('Mined flickr')
hadoopy.launch_frozen(r + 'out/flickr_metadata', r + 'out/flickr_images', 'file_downloader.py')
print('Downloaded images')
