import sys
import web
from threading import Thread
import random
import string
import simplejson as json
import argparse
import os
import Image
import StringIO

if not 'imagedir' in globals():
    imagedir = None


def random_clusters(imagedir, n_clusters=3):
    """Creates a test mockup of random clusters from a folder of images

    Returns:
        clusters: a list of clusters that can be JSONified and passed to the
           html renderer
    """
    image_extensions = set(['jpg', 'png', 'jpeg', 'gif', 'ico'])
    extension = lambda x: x.split('.')[-1] if '.' in x else ''
    local_images = [x for x in sorted(os.listdir(imagedir))
                    if extension(x) in image_extensions]

    clusters = []
    for i in range(n_clusters):
        n_images = random.randrange(4,7)
        n_size = random.randrange(40,60)
        cluster = {'name': [random.choice(string.digits) for _ in range(8)],
                   'all_images': random.sample(local_images, n_size),
                   'sample_images': random.sample(local_images, n_images),
                   'size': n_size}
        clusters.append(cluster)
    return clusters


class Images(object):
    def GET(self, name, extension):
        cType = {
            "png":"images/png",
            "jpg":"image/jpeg",
            "gif":"image/gif",
            "ico":"image/x-icon"
            }
        file_name = '%s.%s' % (name, extension)
        if file_name in os.listdir(imagedir):  # Security
            web.header("Content-Type", cType[extension])  # Set the Header
            return open('%s/%s' % (imagedir, file_name)).read()
        else:
            raise web.notfound()


class Static(object):
    def GET(self, staticdir, name, extension):
        staticdir = '%s/static/%s' % (os.path.dirname(__file__), staticdir)
        cType = {
            "png":"images/png",
            "jpg":"image/jpeg",
            "gif":"image/gif",
            "ico":"image/x-icon",
            "js":"text/javascript",
            "css":"text/css",
            }
        file_name = '%s.%s' % (name, extension)
        if file_name in os.listdir(staticdir):  # Security
            web.header("Content-Type", cType[extension])  # Set the Header
            return open('%s/%s' % (staticdir, file_name)).read()
        else:
            raise web.notfound()


class ThumbImages(object):
    def GET(self, name, extension):
        cType = {
            "png":"images/png",
            "jpg":"image/jpeg",
            "gif":"image/gif",
            "ico":"image/x-icon"
            }
        file_name = '%s.%s' % (name, extension)
        if file_name in os.listdir(imagedir):  # Security
            web.header("Content-Type", cType[extension])  # Set the Header
            img = Image.open('%s/%s' % (imagedir, file_name))
            img.thumbnail((50,50))
            fp = StringIO.StringIO()
            img.save(fp, extension if extension != 'jpg' else 'jpeg')
            fp.seek(0)
            return fp.read()
        else:
            raise web.notfound()


class ShowClusters():
    def GET(self):
        return web.template.frender(os.path.dirname(__file__) +
                                    '/cluster_template.html',
                                    globals=globals())()


if not 'app' in globals():
    urls = ('/', 'ShowClusters',
            '/(css|js|images)/(.*)\.(js|css|png|jpg|gif|ico)', 'Static',
            '/i/(.*)\.(png|jpg|gif|ico)', 'Images',
            '/t/(.*)\.(png|jpg|gif|ico)', 'ThumbImages',
            )
    app = web.application(urls, globals())


def ipython_apprun():
    """For interactive debugging with ipython
    """
    global appthread
    if not 'appthread' in globals():

        def start():
            from IPython.Shell import IPShellEmbed
            IPShellEmbed(user_ns=globals())()
            import thread
            appthread.STOPIT = True
            thread.interrupt_main()

        appthread = Thread(target=start)
        appthread.start()
        appthread.STOPIT = False
        sys.argv = ['', '12546']
        while not appthread.STOPIT:
            try:
                app.run()
            except KeyboardInterrupt:
                continue


def main():
    parser = argparse.ArgumentParser(description='Results Webserver')

    # Webpy port
    parser.add_argument('--port', type=str, help='run webpy on this port',
                        default='12546')

    # Image directory
    parser.add_argument('--imagedir', type=str,
                        help='directory full of images',
                        default='./')

    # K-means clustering
    parser.add_argument('--clusterjs', metavar='<input.js>', type=str,
                        help='load json file containing clusters')

    # Create a sample jsonfile as a random sample of the images
    parser.add_argument('--randomclusters', type=str, metavar='<output.js>',
                        help='Output random cluster json to this file')

    args = parser.parse_args()

    global clusters, imagedir
    imagedir = args.imagedir

    if not args.randomclusters is None:
        # Create random clusters and save them to a file (then exit)
        clusters = random_clusters(args.imagedir)
        with open(args.randomclusters, 'w') as f:
            f.write(json.dumps(clusters))
        print("Wrote %d random clusters to: %s" % \
              (len(clusters), args.randomclusters))
        return

    if not args.clusterjs is None:
        # Read the clusters from a json file
        with open(args.clusterjs, 'r') as f:
            clusters = json.load(f)
    else:
        # Create random clusters using images in the attached directory
        clusters = random_clusters(imagedir)

    sys.argv = ['', args.port]
    app.run()


if __name__ == '__main__':
    #ipython_apprun()
    main()
