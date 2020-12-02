#!/usr/bin/env python3
from setuptools import setup, find_packages


REQUIRES = [
    "dash==1.17.0",
    "dash-bootstrap-components==0.10.7",
    "jupyter==1.0.0",
    "numpy",
    "pandas==0.25.1",
    "rlpyt",
    "rpy2",
    "torch==1.4.0",

    # https://github.com/pallets/flask/issues/1106#issuecomment-67360359
    "flask>=0.10.1",
    "flask-caching",
    "pylibmc",
]


DEPENDENCY_LINKS = [
    "git+https://github.com/astooke/rlpyt.git@f04f23d#egg=rlpyt-0.1.1.dev0",
]


setup(
    name="airlab-retail",
    version="1.0.0",
    description="Library to simulate the ordering policy of a grocery store in order to reduce waste",
    long_description=open("README.md").read(),
    author="Sami Jullien",
    url="https://github.com/samijullien/airlab-retail",
    license="MIT",
    install_requires=REQUIRES,
    dependency_links=DEPENDENCY_LINKS,
)
