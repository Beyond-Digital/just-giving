#!/usr/bin/env python
from setuptools import setup


setup(
    name='just-giving',
    version='0.0',
    description='Just Giving API Client',
    author='Ching Leung',
    author_email='ching.leung@bynd.com',
    url='',
    packages=['just_giving'],
    install_requires=[
        'requests==2.9.0'
    ]
)

