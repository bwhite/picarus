import argparse
import hadoopy
import os
import Image
import hashlib


def copy_with_thumbnails(input_dir, image_dir, thumbnail_dir, limit=1000):

    image_extensions = set(['jpg', 'png', 'jpeg', 'gif', 'ico'])
    extension = lambda x: x.split('.')[-1] if '.' in x else ''
    local_images = ['%s/%s' % (input_dir, x)
                    for x in sorted(os.listdir(input_dir))
                    if extension(x) in image_extensions]

    for filename in local_images:
        with open(filename, 'r') as f:
            data = f.read()

        try:
            im = Image.open(filename)
            im.load()

            md5hash = hashlib.md5(data).hexdigest()
            extension = filename.split('.')[-1]

            #im.save('%s/%s.%s' % (image_dir, md5hash, extension))
            im.thumbnail((100,100))
            im.save('%s/%s.jpg' % (thumbnail_dir, md5hash))
        except (IOError, KeyError):
            #print "couldn't load image: %s" % filename
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Copy images from flickr_data \
    typed bytes files, including thumbnails")

    # Input directory
    parser.add_argument('--inputdir',
                       help='look for part-* in this folder',
                       default='/home/amiller/projects/texas_pete/results_server/images')

    # Fullsize images
    parser.add_argument('--imagedir',
                       help='output images to this folder',
                       default='./i/')

    # Thumbnails
    parser.add_argument('--thumbdir',
                       help='output images to this folder',
                       default='./t/')

    ARGS = parser.parse_args()
    copy_with_thumbnails(ARGS.inputdir, ARGS.imagedir, ARGS.thumbdir)
