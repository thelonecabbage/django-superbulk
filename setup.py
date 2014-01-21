#!/usr/bin/env python
from distutils.core import setup

setup(name="django_superbulk",
      version='0.2',
      description="Django endpoint to enable transactions per request",
      license="GNU",
      author="thelonecabbage",
      url="http://github.com/thelonecabbage/django-superbulk",
      py_modules=['django_superbulk'],
      requires=['django'],
      tests_require=['nose', 'lettuce'],
      keywords="django superbulk transactions")
