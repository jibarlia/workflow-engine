from setuptools import setup, find_packages

setup(
    name="workflow-engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "pytest-asyncio",
    ],
) 