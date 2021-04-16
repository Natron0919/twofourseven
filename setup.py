from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["bs4", "pandas>=1", "requests>=2"]

setup(
    name = "twofourseven",
    version = "0.0.1",
    author = "Nathan Reeb",
    author_email = "Nathan.Reeb94@outlook.com",
    description = "Package to scrape 247Sports website for recruiting data",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Natron0919/TwoFourSeven/",
    packages = find_packages(),
    install_requirements = requirements,
    classifiers = [
        "Programming Language :: Python :: 3.9.1",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)