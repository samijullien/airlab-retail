#!/usr/bin/env python3
from setuptools import setup, find_packages


REQUIRES = [
    # core
    "numpy",
    "pandas==0.25.1",
    "jupyter==1.0.0",
    "torch==1.4.0",

    # UI
    "dash",

    # deep RL
    "rlpyt",

    # misc missing libs
    "flask_caching",
    "Flask",
]


DEPENDENCY_LINKS = [
    "git+https://github.com/astooke/rlpyt.git@f04f23d#egg=rlpyt-0.1.1.dev0",
]


setup(
    name="airlab-retail",
    # version="0.0.1",
    # description="",
    # long_description="",
    # author="Sami Jullien",
    # url="https://github.com/samijullien/airlab-retail",
    # license="MIT",
    # keywords=[],
    install_requires=REQUIRES,
    dependency_links=DEPENDENCY_LINKS,
)
