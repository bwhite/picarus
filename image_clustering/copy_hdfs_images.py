import hadoopy
import argparse
import StringIO
import Image
import os


def dump_images(hdfs_input, local_output):
    for k, image_data in hadoopy.readtb(hdfs_input):
        s = StringIO.StringIO()
        s.write(image_data)
        s.seek(0)
        image = Image.open(s)

        imformat = image.format
        if imformat == 'JPEG': imformat = 'JPG'
        imformat = imformat.lower()
        filename = os.path.join(local_output, '%s.%s' % (k, imformat))

        try:
            os.makedirs(local_output)
        except OSError:
            pass

        with open(filename, 'w') as f:
            f.write(image_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy images from hdfs to a local folder')

    parser.add_argument('hdfs_input', help='get images from hdfs')
    parser.add_argument('local_output', help='copy images here')

    ARGS = parser.parse_args()
    dump_images(ARGS.hdfs_input, ARGS.local_output)
