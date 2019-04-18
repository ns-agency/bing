#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="bing_drive",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask"],
    package_data={"bing_drive": ["templates/*/*", "assets/static/*/*"]},
)
