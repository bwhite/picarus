from fabric.api import run, sudo, put
from fabric.context_managers import cd, settings
import time
import os


def s3_to_hdfs(bucket='bw-hdfs'):
    sudo('apt-get -y install s3cmd')
    put('~/.s3cfg', './')
    hdfs_local = 'hdfs-%f' % time.time()
    hdfs_local = 'hdfs-1325188151.974546'
    with cd('/mnt/tmp'):
        run('mkdir %s' % hdfs_local)
        with cd(hdfs_local):
            run('s3cmd --recursive get s3://%s' % (bucket))
        run('hadoop fs -put %s ./' % hdfs_local)
            

def install_picarus_launcher():
    run('uname -s')
    work_dir = 'picarus-%f' % time.time()
    run('mkdir %s' % work_dir)
    sudo('apt-get -y install libavcodec-dev libswscale-dev libavformat-dev gfortran ffmpeg fftw3-dev python-dev build-essential git-core python-setuptools cmake libjpeg62-dev libpng12-dev libblas-dev liblapack-dev libevent-dev python-scipy python-numpy scons')
    with cd(work_dir):
        # Apt Get
        sudo('easy_install scons cython gevent bottle pil argparse scikit-learn fabric')
        install_git('https://github.com/bwhite/static_server')
        install_git('https://github.com/bwhite/image_server')
        install_git('https://github.com/bwhite/vidfeat')
        install_git('https://github.com/bwhite/imfeat')
        install_git('https://github.com/bwhite/keyframe')
        install_git('https://github.com/bwhite/classipy')
        install_git('https://github.com/bwhite/impoint')
        install_git('https://github.com/bwhite/pyram')
        install_git('https://github.com/bwhite/distpy')
        install_git('https://github.com/bwhite/hadoopy')
        install_git('https://github.com/bwhite/hadoopy_flow')
        install_git('https://github.com/bwhite/picarus')
        run('git clone https://github.com/bwhite/texas_pete')
        install_opencv()

#http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.3.1/OpenCV-2.3.1a.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fopencvlibrary%2F&ts=1325103562&use_mirror=iweb
def install_opencv():
    run('wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.3.1/OpenCV-2.3.1a.tar.bz2')
    # OpenCV
    run('tar -xjf OpenCV-2.3.1a.tar.bz2')
    run('mkdir OpenCV-2.3.1/build')
    with cd('OpenCV-2.3.1/build'):
        run('cmake ..')
        run('make -j8')
        sudo('make install')
        #sudo('cp  lib/cv2.so `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`')  # NOTE(brandyn): Unnecessary ATM


def make_output(path='/mnt/out'):
    print('Making [%s] world writable' % path)
    sudo('mkdir %s' % path)
    sudo('chmod 777 %s' % path)


def install_git(repo):
    run('git clone %s' % repo)
    with cd(os.path.basename(repo)):
        sudo('python setup.py install')
