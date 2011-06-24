import hadoopy
import StringIO
import Image
import json
import matplotlib
matplotlib.use('agg')
import pylab


def hdfs_to_vidjs():
    runs = list(hadoopy.ls('output/video_keyframes'))
    run = runs[-1]
    print run
    for (kind, hash), v in hadoopy.readtb(run):
        if kind == 'frame':
            s = StringIO.StringIO()
            s.write(v)
            s.seek(0)
            frame = Image.open(s)
            frame.save('vid_t/%s.jpg' % hash)
        if kind == 'video':
            with open('videojs/%s.js' % hash, 'w') as f:
                json.dump(v, f)
        if kind == 'scores':
            try:
                pylab.figure(1)
                pylab.clf()
                pylab.plot(v)
                pylab.savefig('scores/%s.png' % hash)
            except Exception, e:
                print e

if __name__ == '__main__':
    hdfs_to_vidjs()
