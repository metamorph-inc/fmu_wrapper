# fmu_wrapper
[![Build status](https://ci.appveyor.com/api/projects/status/usce9x897xurq3oa?svg=true)](https://ci.appveyor.com/project/Metamorph/fmu-wrapper/)

An FMU wrapper for OpenMDAO 1.x

**NOTE: Very early-stage prototype, not yet ready for serious use.**
Suggestions and contributors are welcome.

#### Windows setup (Python 2.7):

    python -m virtualenv fmu_venv
    fmu_venv\scripts\activate
    pip install -r requirements.txt
    nosetests
