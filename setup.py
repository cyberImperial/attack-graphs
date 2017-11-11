# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='attack-graphs',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "requests==2.9.1",
        "pcapy"
    ],
    tests_require=[
    ],
    test_suite='tests',
    zip_safe=False,
)
