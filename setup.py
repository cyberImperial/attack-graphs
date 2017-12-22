# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='attack-graphs',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "pcapy",
        "requests>=2.9.1",
        "clint"
    ],
    tests_require=[
        "timeout_decorator"
    ],
    test_suite='tests',
    zip_safe=False,
)
