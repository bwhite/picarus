Takeout
=======

Overview
--------


Windows
--------

CMake
+++++
http://www.cmake.org/cmake/resources/software.html

Visual Studio
++++++++++++++
Visual Studio (tested on C++ 2010 Express).
https://www.microsoft.com/visualstudio/eng/downloads

OpenCV
++++++
MAKE SURE TO USE RELEASE MODE IN VISUAL STUDIO! OpenCV won't work without it.
http://sourceforge.net/projects/opencvlibrary/files/opencv-win/
http://docs.opencv.org/doc/tutorials/introduction/windows_install/windows_install.html#windowssetpathandenviromentvariable

PThreads
++++++++
ftp://sourceware.org/pub/pthreads-win32/prebuilt-dll-2-9-1-release

Msgpack
+++++++
http://www.7-zip.org/ (for opening up the .tar.gz)
http://sourceforge.net/projects/msgpack/files/msgpack/cpp/

Convert the project, build it.

A few problems need to be fixed
https://github.com/qehgt/myrpc/issues/3

*  Move type.hpp from include\msgpack\type into include\msgpack
*  Replace this file https://raw.github.com/msgpack/msgpack-c/master/sysdep.h

FFTW
++++

http://www.fftw.org/install/windows.html
http://www.fftw.org/fftw-3.3.3.tar.gz
