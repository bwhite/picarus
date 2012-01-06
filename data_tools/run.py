import hadoopy
import time

r = 'flickr_data/run-%f/' % time.time()
tags = 'christmas flower rose bird tree'
hadoopy.writetb(r + 'tags', enumerate(tags.split()))
print('Wrote tags')
hadoopy.launch_frozen(r + 'tags', r + 'out/flickr_metadata', 'flickr_bulk.py')
print('Mined flickr')
hadoopy.launch_frozen(r + 'out/flickr_metadata', r + 'out/flickr_images', 'file_downloader.py')
print('Downloaded images')
