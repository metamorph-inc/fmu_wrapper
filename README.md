# fmu_wrapper
[![Build status](https://ci.appveyor.com/api/projects/status/dys2woikuo5fstio/branch/master?svg=true)](https://ci.appveyor.com/project/ksmyth/fmu-wrapper/branch/master)

An FMU wrapper for OpenMDAO 1.x

**NOTE: Very early-stage prototype, not yet ready for serious use.**
Suggestions and contributors are welcome.

#### Windows setup (Python 2.7):

    python -m virtualenv fmu_venv
    fmu_venv\scripts\activate
    pip install -r requirements.txt
    pip install --index-url https://pypi.metamorphsoftware.com/ Assimulo==2.9
    pip install nose
    nosetests
