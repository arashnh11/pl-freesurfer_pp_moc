import sys
import os
# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup


def readme():
    print("Current dir = %s" % os.getcwd())
    print(os.listdir())
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'freesurfer_pp_moc',
      version          =   '2.2.0',
      description      =   'A simple/dummy app that simulates a FreeSurfer run', 
      long_description =   readme(),
      author           =   'Rudolph Pienaar',
      author_email     =   'rudolph.pienaar@gmail.com',
      url              =   'https://github.com/FNNDSC/pl-freesurfer_pp_moc',
      packages         =   ['freesurfer_pp_moc'],
      install_requires =   ['chrisapp', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['freesurfer_pp_moc/freesurfer_pp_moc.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
