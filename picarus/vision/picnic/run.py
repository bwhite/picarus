import hadoopy
import os

r = 'hadoopy-picnic/'
#r = 'picnic/0/'
tags = 'christmas flower rose bird tree'
#hadoopy.writetb(r + 'tags', enumerate(tags.split()))
print('Wrote tags')
#hadoopy.launch_frozen(r + 'tags', r + 'out/flickr_metadata', 'flickr_bulk.py')
print('Mined flickr')
#hadoopy.launch_local(r + 'out/flickr_metadata', r + 'out/flickr_images', 'file_downloader.py',
#                     worker_queue_maxsize=10)  # , max_input=100
print('Downloaded images')
hadoopy.launch_frozen('flickr_data_picarus/run-1343712226.822338/out/flickr_images', r + 'tiles', 'picnic_job.py',
                      files=['target.jpg'], remove_output=True)
try:
    os.makedirs('tiles')
except OSError:
    pass
for k, v in hadoopy.readtb(r + 'tiles'):
    with open('tiles/' + k, 'w') as fp:
        fp.write(v)
