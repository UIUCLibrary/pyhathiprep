from setuptools import setup

setup(
    name="pyhathiprep",
    packages=['pyhathiprep'],
    install_requires=[
        "ruamel.yaml",
        "pytz",
        "tzlocal<5.0",
        'importlib_resources;python_version<"3.7"',
        'typing-extensions;python_version<"3.10"'
    ],
    package_data={"pyhathiprep": ["py.typed"]},
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
         "console_scripts": [
             'pyhathiprep = pyhathiprep.__main__:main'
         ]
     },
)
