import argparse
import web
import sys
import os
import Image
import hashlib
from threading import Thread
import StringIO
import imfeat
import cass
import json
import time

if not 'app' in globals():
    urls = ('/features/(.*)/(.*)', 'Features',
            '/features', 'Features',
            '/i/(.*)', 'Images',
            '/t/(.*)', 'ThumbImages',
            '/', 'Main',
            )
    app = web.application(urls, globals())


class Main(object):
    def GET(self):
        web.header("Content-Type", "text/html")
        return '<img src="/i/5eea8baf274a78fbb16ad7f99300acd7"/>'


class Features(object):
    def GET(self, feature_id=None, image_id=None):
        if feature_id is None and image_id is None:
            web.header("Content-Type", "text/plain")
            return json.dumps(cass.get_available_features())


class Images(object):
    def GET(self, md5hash):
        cType = {
            "PNG":"images/png",
            "JPEG":"image/jpeg",
            "GIF":"image/gif",
            "ICO":"image/x-icon"
            }
        try:
            data = cass.get_imagedata(md5hash)
        except KeyboardInterrupt:
            raise web.notfound()

        try:
            s = StringIO.StringIO(data)
            im = Image.open(s)
        except IOError:
            raise web.internalerror('Couldn\' open image')

        web.header("Content-Type", cType[im.format])  # Set the Header
        return data


class ThumbImages(object):
    def GET(self, md5hash):
        cType = {
            "PNG":"images/png",
            "JPEG":"image/jpeg",
            "GIF":"image/gif",
            "ICO":"image/x-icon"
            }
        try:
            data = cass.get_imagedata(md5hash)
        except KeyboardInterrupt:
            raise web.notfound()

        try:
            s = StringIO.StringIO(data)
            im = Image.open(s)
        except IOError:
            raise web.internalerror('Couldn\'t open image %s' % md5hash)

        web.header("Content-Type", cType['JPEG'])  # Set the Header
        fp = StringIO.StringIO()
        im.thumbnail(100,50)
        im.save(fp, 'JPEG')
        fp.seek(0)
        return fp.read()


def ipython_apprun():
    """For interactive debugging with ipython
    """
    global appthread
    if not 'appthread' in globals():

        def start():
            from IPython.Shell import IPShellEmbed
            IPShellEmbed(argv=[], user_ns=globals())()
            import thread
            appthread.STOPIT = True
            thread.interrupt_main()

        appthread = Thread(target=start)
        appthread.start()
        appthread.STOPIT = False
        sys.argv = ['', ARGS.port]
        while not appthread.STOPIT:
            try:
                app.run()
            except KeyboardInterrupt:
                continue


def put_images(imagedir):
    success_count = 0
    for filename in os.listdir(imagedir):
        try:
            with open(os.path.join(imagedir, filename), 'r') as f:
                data = f.read()
            import StringIO
            s = StringIO.StringIO(data)
            im = Image.open(s)
            im.verify()
        except IOError:
            print "couldn't load image: %s" % filename
            continue

        md5hash = hashlib.md5(data).hexdigest()

        # Store the image file indexed by hash
        cass.put_image(md5hash, data)
        success_count += 1
        print 'Put %s (%s)' % (filename, md5hash)
    total = len(cass.get_image_hashes())
    print 'Successfully put %d images (total %d)' % (success_count, total)


def put_features(feature_str, hashes=None):
    feature = eval(feature_str, {'imfeat': imfeat})
    print('Feature: %s (%s)' % (feature_str, feature))

    # Compute feature on all available images by default
    if hashes is None:
        hashes = cass.get_image_hashes()

    print('Computing feature for %d images' % len(hashes))
    success_count = 0
    start_time = time.time()
    for md5hash in hashes:
        data = cass.get_imagedata(md5hash)
        import StringIO
        s = StringIO.StringIO(data)

        try:
            im = Image.open(s)
            im.load()
        except IOError:
            print "couldn't load image: %s" % md5hash
            continue

        im = im.convert("RGB")
        # Compute the feature
        value = imfeat.compute(feature, im)
        ret = cass.put_feature_value(feature_str, md5hash, value)
        print("Put feature_value([%s], [%s]): %d" % (feature_str,
                                                     md5hash, ret))
        success_count += 1
    stop_time = time.time()
    print("Finished %d features in %.2f seconds" % \
          (success_count, stop_time-start_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve images and features \
    from Cassandra")

    # Webpy port
    parser.add_argument('--port', type=str, help='run webpy on this port',
                        default='8080')

    # Optional IPython shell
    parser.add_argument('--ipython', action='store_true',
                        help="Run an IPython shell for debugging")

    # Load images into cassandra
    parser.add_argument('--put_images',
                        help='Put a directory of images to Cassandra',
                        default=None)

    # Compute features and load values to cass
    group = parser.add_argument_group('compute_features')
    group.add_argument('--compute_features',
                       help='expression returning an imfeat feature')

    ARGS = parser.parse_args()

    cass.connect()

    if not ARGS.put_images is None:
        print 'Putting images from %s to Cassandra' % ARGS.put_images
        put_images(ARGS.put_images)
        sys.exit(0)

    if not ARGS.compute_features is None:
        print 'Computing features'
        put_features(ARGS.compute_features)
        sys.exit(0)

    if ARGS.ipython:
        ipython_apprun()
    else:
        sys.argv = ['', ARGS.port]
        app.run()
