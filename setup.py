from setuptools import setup

setup(
    name="pyhathiprep",
    packages=['pyhathiprep'],
    install_requires=[
        "ruamel.yaml",
        "pytz",
        "tzlocal",
        'importlib_resources;python_version<"3.7"'
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
