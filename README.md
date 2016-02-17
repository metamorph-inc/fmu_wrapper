# fmu_wrapper
An FMU wrapper for OpenMDAO 1.x

**NOTE: Very early-stage prototype, not yet ready for serious use.**
Suggestions and contributors are welcome.

#### Windows setup (Python 2.7):

These instructions were created from https://pypi.python.org/pypi/PyFMI  
Download:  
FMILibrary-2.0.1-win32.zip from http://www.jmodelica.org/FMILibrary  
numpy, scpipy, Assimulo-2.8-cp27-none-win32.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/  
%userprofile%\Documents\OpenMDAO

    python -m virtualenv fmu_venv
    fmu_venv\scripts\activate
    pip install %userprofile%\Downloads\numpy-1.10.1+mkl-cp27-none-win32.whl
    pip install %userprofile%\Downloads\scipy-0.16.1-cp27-none-win32.whl
    pip install -i https://pypi.metamorphsoftware.com/ lxml
    pip install %userprofile%\Downloads\Assimulo-2.8-cp27-none-win32.whl
    "\Program Files\7-Zip\7z.exe" x -y "%userprofile%\Downloads\FMILibrary-2.0.1-win32.zip"
    set FMIL_HOME=%CD%\FMILibrary-2.0.1-win32\
    setx FMIL_HOME "%CD%\FMILibrary-2.0.1-win32"\
    pip install cython
    pip install pylab
    pip install pyfmi
    pip install -e %userprofile%\Documents\OpenMDAO
    python src\fmu_wrapper\fmu_wrapper.py
