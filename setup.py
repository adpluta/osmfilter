# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="SciGRID-OSM-filter",
    version="1.0.0",
    description="filtering of OSM pbf-files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/osmfilter",
    author="Adam Pluta",
    author_email="Adam.Pluta@dlr.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
     python_requires='>=3.6',
            
)