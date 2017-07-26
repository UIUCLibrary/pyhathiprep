from setuptools import setup
import os

about = {}

metadata_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pyhathiprep', '__version__.py')

with open(metadata_file, 'r', encoding='utf-8') as f:
    exec(f.read(), about)
with open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    packages=['pyhathiprep'],
    url=about["__url__"],
    license='University of Illinois/NCSA Open Source License',
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=readme,
    install_requires=[
        "ruamel.yaml",
        "pytz",
        "tzlocal"
    ],
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
         "console_scripts": [
             'pyhathiprep = pyhathiprep.__main__:main'
         ]
     },
)
