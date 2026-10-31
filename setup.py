#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name='django-altair',
    version='1.1.0',
    description='Altair widget for Django',

    author='Jesse Hinrichsen',
    author_email='jesse.hinrichsen@gmail.com',
    url='https://github.com/jesse-japps/django-altair/',

    packages=find_packages(exclude=['example.*', 'example', 'tests', 'tests.*']),
    include_package_data=True,  # declarations in MANIFEST.in

    python_requires='>=3.10',
    install_requires=['Django>=5.2'],
    license='BSD-3-Clause',
)
