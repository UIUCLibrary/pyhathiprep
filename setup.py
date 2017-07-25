from setuptools import setup
import pyhathiprep

with open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name=pyhathiprep.__title__,
    version=pyhathiprep.__version__,
    packages=['pyhathiprep'],
    url=pyhathiprep.__url__,
    license='University of Illinois/NCSA Open Source License',
    author=pyhathiprep.__author__,
    author_email=pyhathiprep.__author_email__,
    description=pyhathiprep.__description__,
    long_description=readme,
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
         "console_scripts": [
             'pyhathiprep = pyhathiprep.__main__:main'
         ]
     },
)
