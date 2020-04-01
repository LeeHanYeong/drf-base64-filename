#!/usr/bin/env python
import os
from setuptools import find_packages, setup

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
README = open(os.path.join(ROOT_DIR, 'README.md')).read()
VERSION = open(os.path.join(ROOT_DIR, 'version.txt')).read()

setup(
    name='drf-base64-filename',
    version=VERSION,
    description='drf-base64-filename provides Serializer fields for using base64-encoded files with file names.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='LeeHanYeong',
    author_email='dev@lhy.kr',
    license='MIT',
    packages=find_packages(exclude=['test*', 'sample', 'demo']),
    install_requires=[
        'django',
        'djangorestframework',
        'django-extra-fields',
    ],
    python_requires=">3.5",
    url='https://github.com/LeeHanYeong/drf-base64-filename',
    zip_safe=True,
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
    ]
)
