from setuptools import find_packages, setup

from datacli import __version__

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="dataclass-cli",
    version=__version__,
    packages=find_packages(exclude=("tests",)),

    author="Jeremy Stafford",
    author_email="jeremyspianopenguin@gmail.com",
    description="A library for building simple CLIs from dataclasses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jeremy-Stafford/datacli",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
