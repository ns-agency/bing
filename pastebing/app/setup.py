#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="pastebing",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask"],
    package_data={"pastebing": ["templates/*/*", "assets/static/*/*"]},
)
