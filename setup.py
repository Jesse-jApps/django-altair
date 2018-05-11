#!/usr/bin/env python
import re

from setuptools import find_packages, setup


setup(
    name='django-altair',
    version=1.0,
    description='Altair widget for Django',

    author='Jesse Hinrichsen',
    author_email='jesse.hinrichsen@gmail.com',
    url='https://github.com/jesse-japps/django-altair/',

    packages=find_packages(exclude=['example.*', 'example']),
    include_package_data=True,  # declarations in MANIFEST.in

    install_requires=['Django>=1.11']
)