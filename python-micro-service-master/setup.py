#!/usr/bin/env python

import json
from setuptools import setup

requirements = set()

with open("Pipfile.lock") as pipfile_lock:
    for name, attr in json.load(pipfile_lock)["default"].items():
        if "version" in attr:
            requirements.add(f"{name}{attr.get('version', '')}")


setup(install_requires=list(requirements))
