from setuptools import setup, find_packages

setup(
    # Application name:
    name="visci",

    # Version number (initial):
    version="0.1",

    # Application author details:
    author="Vanessa Sochat",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=find_packages(),

    # Details
    url="http://www.github.com/vsoch/visualization-ci",

    install_requires = ["cognitiveatlas","Jinja2"],

    license="LICENSE.txt",
    description="visualization standard file structure for continuous integration",

)
