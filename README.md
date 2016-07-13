# fmu_wrapper
An FMU wrapper for OpenMDAO 1.x

**NOTE: Very early-stage prototype, not yet ready for serious use.**
Suggestions and contributors are welcome.

#### Windows setup (Python 2.7):

    python -m virtualenv fmu_venv
    fmu_venv\scripts\activate
    "\Program Files\7-Zip\7z.exe" x -y "%userprofile%\Downloads\FMILibrary-2.0.1-win32.zip"
    set FMIL_HOME=%CD%\FMILibrary-2.0.1-win32\
    setx FMIL_HOME "%CD%\FMILibrary-2.0.1-win32"\
    pip install -r requirements.txt
    pip install --index-url https://pypi.metamorphsoftware.com/ Assimulo==2.9
    pip install nose
    nosetests
