#!/usr/bin/env python3
"""
Setup script for TermTweet - Python package installation
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="termtweet",
    version="1.0.0",
    author="TermTweet",
    author_email="",
    description="A simple CLI tool to tweet from your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/termtweet",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Communications",
        "Topic :: Utilities",
    ],
    keywords="twitter cli terminal tweet development",
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "termtweet=termtweet.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/yourusername/termtweet/issues",
        "Source": "https://github.com/yourusername/termtweet",
        "Documentation": "https://github.com/yourusername/termtweet#readme",
    },
)