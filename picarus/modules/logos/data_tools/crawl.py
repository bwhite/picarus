import logging
logging.basicConfig(level=logging.DEBUG)
import vision_data.hadoop
import glob
import os


def main(image_path):
    tags = []
    for image_path in glob.glob(image_path + '/*'):
        tags.append(os.path.basename(image_path).rsplit('.', 1)[0] + ' logo')
    vision_data.hadoop.flickr_images(tags, 500, 'flickr/logos/', remove_output=True, max_pages=3)


if __name__ == '__main__':
    main('/home/brandyn/projects/crawlers/goodlogo/images/')
