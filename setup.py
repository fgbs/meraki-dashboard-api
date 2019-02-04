#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='meraki-dashboard-api',
    version='1.0.0',
    author='Felipe Barros',
    author_email='felipe.barros@gmail.com',
    description='Meraki Dashboard API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fgbs/meraki-dashboard-api',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'requests-toolbelt',
        'urllib3'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Networking'
    ]
)