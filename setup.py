from setuptools import find_packages, setup

from datacli import __version__

setup(
    name="dataclass-cli",
    version=__version__,
    packages=find_packages(),

    author="Jeremy Stafford",
    author_email="jeremyspianopenguin@gmail.com",
    description="A library for building simple CLIs from dataclasses",
    keywords="dataclass cli",
    url="https://github.com/Jeremy-Stafford/datacli",
    classifies=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)
