#!/usr/bin/env python3
"""
Script de configuration pour créer un paquet installable
Utilisation : python3 setup.py sdist bdist_wheel
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="password-manager-secure",
    version="1.0.0",
    author="Your Name",
    description="Un gestionnaire de mots de passe sécurisé et hors ligne",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/password-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "password-manager=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
)
