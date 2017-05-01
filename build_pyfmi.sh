#!/bin/bash -x

set -e
set -u

echo Using $FMIL_HOME . Be sure it matches the Python architecture

for pythondir in /c/Python27/ /c/Python36/; do
#for pythondir in /c/Python27-x64/ /c/Python36-x64/; do
# for pythondir in /c/Python36-x64/; do
# for pythondir in /c/Python27/ /c/Python27-x64/ /c/Python35/ /c/Python35-x64/; do
# for pythondir in /c/Python27-x64/ /c/Python35/ /c/Python35-x64/; do
# for pythondir in /c/Python35/ ; do
# for pythondir in /c/Python27-x64/ /c/Python35-x64/; do
# for pythondir in /c/Python35-x64/; do
[ -d venv ] && rm -rf venv
${pythondir}/python -m virtualenv venv
grep -Eiv "(pylab|PyFMI)" requirements.txt > pyfmi_requirements.txt
./venv/scripts/pip install --process-dependency-links Cython -r pyfmi_requirements.txt
# ./venv/scripts/pip wheel --no-cache-dir --isolated PyFMI
# cd PyFMI-2.4.0
cd PyFMI-2.4
git clean -xdf
../venv/Scripts/python setup.py bdist_wheel
cp dist/*.whl ../
cd ..
done


exit 0

Download:  
FMILibrary-2.0.1-win32.zip from http://www.jmodelica.org/FMILibrary  
http://www.jmodelica.org/downloads/FMIL/FMILibrary-2.0.2-win32.zip
"\Program Files\7-Zip\7z.exe" x -y "%userprofile%\Downloads\FMILibrary-2.0.1-win32.zip"
set FMIL_HOME=%CD%\FMILibrary-2.0.1-win32\
set FMIL_HOME=%CD%\FMILibrary-2.0.1-x64\
grep -Eiv "(pylab|PyFMI)" requirements.txt > pyfmi_requirements.txt
python -m virtualenv venv
venv\scripts\activate
pip install -r requirements.txt
pip wheel --no-cache-dir --isolated PyFMI

diff --git a/setup.py b/setup.py
index 439e842..3df7ce7 100644
--- a/setup.py
+++ b/setup.py
@@ -17,9 +17,10 @@

 #from distutils.core import setup, Extension
 #from distutils.ccompiler import new_compiler
-from distutils.core import setup
-
-import distutils
+#from distutils.core import setup
+from setuptools import setup
+import setuptools as distutils
+#import distutils
 import os as O
 import sys as S
 import shutil

 
FMILibrary build:

set PATH=%PATH%;c:\Program Files (x86)\CMake\bin
cmake -G "Visual Studio 10" "%CD%\.."
cmake --build . --config MinSizeRel --target install

diff --git a/ThirdParty/Zlib/zlib-1.2.6/gzlib.c b/ThirdParty/Zlib/zlib-1.2.6/gzlib.c
index 7aedab8..700b6f4 100644
--- a/ThirdParty/Zlib/zlib-1.2.6/gzlib.c
+++ b/ThirdParty/Zlib/zlib-1.2.6/gzlib.c
@@ -4,7 +4,7 @@
  */
 
 #include "gzguts.h"
-
+#include <io.h>
 #if defined(_WIN32) && !defined(__BORLANDC__)
 #  define LSEEK _lseeki64
 #else
diff --git a/ThirdParty/Zlib/zlib-1.2.6/gzread.c b/ThirdParty/Zlib/zlib-1.2.6/gzread.c
index 46d40e0..64f5275 100644
--- a/ThirdParty/Zlib/zlib-1.2.6/gzread.c
+++ b/ThirdParty/Zlib/zlib-1.2.6/gzread.c
@@ -4,7 +4,7 @@
  */
 
 #include "gzguts.h"
-
+#include <io.h>
 /* Local functions */
 local int gz_load OF((gz_statep, unsigned char *, unsigned, unsigned *));
 local int gz_avail OF((gz_statep));
diff --git a/ThirdParty/Zlib/zlib-1.2.6/gzwrite.c b/ThirdParty/Zlib/zlib-1.2.6/gzwrite.c
index caa35b6..1214d34 100644
--- a/ThirdParty/Zlib/zlib-1.2.6/gzwrite.c
+++ b/ThirdParty/Zlib/zlib-1.2.6/gzwrite.c
@@ -5,6 +5,7 @@
 
 #include "gzguts.h"
 
+#include <io.h>
 /* Local functions */
 local int gz_init OF((gz_statep));
 local int gz_comp OF((gz_statep, int));
