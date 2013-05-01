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


Include/Library Paths
++++++++++++++++++++++
An example of all of the paths, libraries, and command line arguments can be found here https://gist.github.com/bwhite/5493885

Building
+++++++++
* Use cmake to create a directory (e.g., /build) by pointed its source input at the inner picarus_takeout folder (has the CMakeLists.txt file) and clicking "generate".
* Go into build, open picarus.vcxproj.
* Change to release mode.  In the solution explorer, right click on picarus, go to properties.
* In VC++ Directories/Include Directories add all of the include dirs.
* For opencv make sure to include every single directory in modules/*/include (lots of copy and pasting)
* Under linker/general, add the library paths under "Additional Library Directories".
* Close that window, right click on picarus, go to build.
* You will need a 1.) a picarus model (if you need one ask me) and an input is an image
* Copy the model and input image into the /build/Release directory.
* Either 1.) copy all the dll's into the /build/Release directory or 2.) make sure windows knows where to find them.
* Go into the /build/Release directory in a terminal, and type  "picarus <model> <input> <output>"
* Model is the picarus model, input is an image, and output is where to store the output file
* If everything worked, you'll have a new output file at the path you specified, it is in msgpack format.
