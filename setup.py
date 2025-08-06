#!/usr/bin/env python3
"""
Setup script for DynaMix
Advanced Audio Transition Analysis Tool for DJs
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Get version
def get_version():
    version_file = os.path.join("dynamix", "__init__.py")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "0.1.0"

setup(
    name="dynamix",
    version=get_version(),
    author="makalin",
    author_email="your.email@example.com",
    description="Advanced Audio Transition Analysis Tool for DJs",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/makalin/dynamix",
    project_urls={
        "Bug Tracker": "https://github.com/makalin/dynamix/issues",
        "Documentation": "https://github.com/makalin/dynamix/docs",
        "Source Code": "https://github.com/makalin/dynamix",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Players :: MP3",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    keywords="audio analysis dj mixing music transition bpm key detection",
    packages=find_packages(),
    py_modules=[
        "mix_analiz",
        "mix_enhanced", 
        "audio_utils",
        "playlist_manager",
        "dj_tools",
        "examples"
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "coverage>=7.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "pylint>=2.17.0",
            "mypy>=1.0.0",
            "bandit>=1.7.0",
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "pre-commit>=3.0.0",
            "twine>=4.0.0",
            "wheel>=0.40.0",
        ],
        "full": [
            "librosa[all]>=0.10.0",
            "soundfile>=0.12.0",
            "pydub>=0.25.0",
            "scipy>=1.10.0",
            "scikit-learn>=1.3.0",
            "plotly>=5.0.0",
            "bokeh>=3.0.0",
            "tqdm>=4.65.0",
            "click>=8.1.0",
            "rich>=13.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "coverage>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dynamix=mix_enhanced:main",
            "dynamix-basic=mix_analiz:main",
            "dynamix-dj=dj_tools:main",
            "dynamix-examples=examples:main",
        ],
    },
    include_package_data=True,
    package_data={
        "dynamix": [
            "*.md",
            "*.txt",
            "*.yml",
            "*.yaml",
            "*.json",
        ],
    },
    data_files=[
        ("share/dynamix", [
            "README.md",
            "LICENSE",
            "requirements.txt",
            "requirements-dev.txt",
        ]),
        ("share/dynamix/examples", [
            "examples.py",
        ]),
        ("share/dynamix/docs", [
            "docs/README.md",
        ]),
    ],
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    maintainer="makalin",
    maintainer_email="your.email@example.com",
    provides=["dynamix"],
    requires_python=">=3.8",
    setup_requires=[
        "setuptools>=45.0.0",
        "wheel>=0.37.0",
    ],
    test_suite="tests",
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
    ],
    options={
        "bdist_wheel": {
            "universal": True,
        },
    },
) 