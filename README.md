# fmu_wrapper
An FMU wrapper for OpenMDAO 1.x


#### Windows setup (Python 2.7):

These instructions were created from https://pypi.python.org/pypi/PyFMI  
Download:  
FMILibrary-2.0.1-win32.zip from http://www.jmodelica.org/FMILibrary  
Assimulo-2.8.win32-py2.7.exe from https://pypi.python.org/pypi/Assimulo  
%userprofile%\Documents\OpenMDAO

    python -m virtualenv --system-site-packages fmu_venv
    fmu_venv\scripts\activate
    pip install -i https://pypi.metamorphsoftware.com/ numpy
    pip install -i https://pypi.metamorphsoftware.com/ scipy
    pip install -i https://pypi.metamorphsoftware.com/ lxml
    "\Program Files\7-Zip\7z.exe" x -y "%userprofile%\Downloads\FMILibrary-2.0.1-win32.zip"
    set FMIL_HOME=%CD%\FMILibrary-2.0.1-win32\
    setx FMIL_HOME "%CD%\FMILibrary-2.0.1-win32"\
    rem unfortunately, this won't pip install. TODO: fix it
    start /wait %userprofile%\Downloads\Assimulo-2.8.win32-py2.7.exe
    pip install cython
    pip install pylab
    pip install pyfmi
    pip install -e %userprofile%\Documents\OpenMDAO
    python src\fmu_wrapper\fmu_wrapper.py

    TODO: virtualenv doesn't need --system-site-packages if:
    echo c:\Python27\lib\site-packages > C:\Users\kevin\Documents\fmu_wrapper\fmu_venv\Lib\site-packages\assimulo.pth
    TODO: remove it from sys.path ? import assimulo; import sys; sys.path.remove(r'c:\Python27\lib\site-packages')
