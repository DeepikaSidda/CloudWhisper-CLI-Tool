#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cloudwhisper",
    version="1.0.0",
    author="CloudWhisper Team",
    author_email="<email>",
    description="AI-powered AWS infrastructure and cost optimization CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/<username>/cloudwhisper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "boto3>=1.26.0",
        "botocore>=1.29.0",
        "openai>=1.0.0",
        "rich>=13.0.0",
        "tabulate>=0.9.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.0",
        "jinja2>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cloudwhisper=cloudwhisper.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
