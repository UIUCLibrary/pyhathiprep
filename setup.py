from setuptools import setup

setup(
    packages=['pyhathiprep'],
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
