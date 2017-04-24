from setuptools import setup

kwargs = {'author': 'Adam Nagel',
          'author_email': 'adam.nagel@gmail.com',
          'classifiers': ['Intended Audience :: Science/Research',
                          'Topic :: Scientific/Engineering'],
          'description': 'OpenMDAO Wrapper for FMU',
          'download_url': '',
          'entry_points': '[openmdao.component]\nfmu_wrapper.FmuWrapper=fmu_wrapper:FmuWrapper\n\n[openmdao.container]\nfmu_wrapper.FmuWrapper=fmu_wrapper:FmuWrapper',
          'include_package_data': True,
          'install_requires': ['openmdao', 'pyfmi', 'Assimulo'],
          'keywords': ['openmdao, fmu'],
          'license': 'GNU General Public License, version 2',
          'maintainer': 'Adam Nagel',
          'maintainer_email': 'adam.nagel@gmail.com',
          'name': 'fmu_wrapper',
          'packages': ['fmu_wrapper', 'fmu_wrapper.test'],
          'package_dir': {'fmu_wrapper': 'fmu_wrapper'},
          'package_data': {'fmu_wrapper.test': ['test/bouncingBall.fmu']},
          'url': 'https://github.com/metamorph-inc/fmu_wrapper',
          'version': '0.2',
          'zip_safe': False}

setup(**kwargs)
