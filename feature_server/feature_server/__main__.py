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
import itertools

import train_test_runs

if not 'app' in globals():
    urls = ('/features/(.*)/(.*)', 'Features',
            '/features', 'Features',
            '/i/(.*)', 'Images',
            '/t/(.*)', 'ThumbImages',
            '/', 'Main',
            '/test_runs/', 'Classifier',
            '/test_runs/(.+)', 'Classifier',
            )
    app = web.application(urls, globals())


class Classifier():
    def GET(self, run=None):
        if run is None:
            # TODO display the list of runs with a new template
            runs = train_test_runs.available_runs()
            return ["<a href='/classifier/runs/%s'>%s</a>" % \
                    run for run in runs]

        run_list = train_test_runs.get_run(run)
        """run_list is a list of [(label, [confidence, GT, hash]), ...]
        where GT is ground truth annotation, -1 or 1.
        """


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


def put_images(imagedir, replace=False):
    success_count = 0
    filenames = os.listdir(imagedir)
    old_hashes = set(cass.get_image_hashes() if not replace else [])

    for filename in filenames:
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
        if md5hash in old_hashes:
            continue

        # Store the image file indexed by hash
        cass.put_image(md5hash, data,
                       metadata={
                           'filename': filename,
                           })
        success_count += 1
        print 'Put %s (%s)' % (filename, md5hash)
    total = len(list(cass.get_image_hashes()))
    print 'Successfully put %d images (total %d)' % (success_count, total)


def put_features(feature_str, hashes=None, replace=False):
    feature = eval(feature_str, {'imfeat': imfeat})
    print('Feature: %s (%s)' % (feature_str, feature))

    # Compute feature on all available images by default
    if hashes is None:
        hashes = cass.get_image_hashes()

    # Optionally try not to replace existing features
    if replace:
        print 'Replacing all existing features for %s' % feature_str
    else:
        old_hashes = cass.get_feature_hashes(feature_str)

    # Get an estimate of the number of images by counting
    # FIXME This requires cass to load the whole row, twice
    if 1:
        print ('Computing feature for %d images' % \
               len(list(cass.get_feature_hashes(feature_str))))

    success_count = 0
    start_time = time.time()

    _hashes = hashes if replace else cass.sorted_iter_diff(hashes, old_hashes)
    for md5hash in _hashes:
        data = cass.get_imagedata(md5hash)
        import StringIO
        s = StringIO.StringIO(data)

        try:
            im = Image.open(s)
            im.load()

            # Guard for small images that break GIST
            if im.size[0] < 10 or im.size[1] < 10 or \
                   im.size[0] > 1000 or im.size[1] > 1000:
                print('Skipping small image (%d, %d) because of \
                GIST segfault' % im.size)
                continue

        except IOError:
            print "couldn't load image: %s" % md5hash
            continue

        # FIXME this seems to be necessary for many features
        # e.g. imfeat.Moments and imfeat.GIST()
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

    # Don't replace
    parser.add_argument('--replace', action='store_true',
                       help='don\'t replace existing image or feature')

    # Optional IPython shell
    parser.add_argument('--ipython', action='store_true',
                        help="Run an IPython shell for debugging")

    # Load images into cassandra
    group = parser.add_argument_group('put_images')
    parser.add_argument('--put_images',
                        help='Put a directory of images to Cassandra')

    # Compute features and load values to cass
    group = parser.add_argument_group('compute_features')
    group.add_argument('--compute_features',
                       help='expression returning an imfeat feature')

    ARGS = parser.parse_args()

    cass.connect()

    if not ARGS.put_images is None:
        print 'Putting images from %s to Cassandra' % ARGS.put_images
        put_images(ARGS.put_images, ARGS.replace)
        sys.exit(0)

    if not ARGS.compute_features is None:
        print 'Computing features'
        put_features(ARGS.compute_features, replace=ARGS.replace)
        sys.exit(0)

    if ARGS.ipython:
        ipython_apprun()
    else:
        sys.argv = ['', ARGS.port]
        app.run()
