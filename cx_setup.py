import os
import sys
from setuptools.config import read_configuration
import cx_Freeze
import pytest
import platform


def get_project_metadata():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "setup.cfg"))
    return read_configuration(path)["metadata"]

metadata = get_project_metadata()


def create_msi_tablename(python_name, fullname):
    shortname = python_name[:6].replace("_", "").upper()
    longname = fullname
    return "{}|{}".format(shortname, longname)


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
MSVC = os.path.join(PYTHON_INSTALL_DIR, 'vcruntime140.dll')


def get_tests():
    root = "tests"
    test_files = []
    for x in filter(lambda x: x.is_file and os.path.splitext(x.name)[1] == ".py", os.scandir(root)):
        relative_path = os.path.join(root, x.name)
        absolute_path = x.path
        test_files.append((absolute_path, relative_path))
    print("Found files {}".format(", ".join(x[0] for x in test_files)))
    return test_files


INCLUDE_FILES = [
    "documentation.url",
    "setup.cfg"
] + get_tests()

directory_table = [
    (
        "ProgramMenuFolder",  # Directory
        "TARGETDIR",  # Directory_parent
        "PMenu|Programs",  # DefaultDir
    ),
    (
        "PMenu",  # Directory
        "ProgramMenuFolder",  # Directory_parent
        create_msi_tablename(metadata["name"], "PyHathiPrep")
    ),
]
shortcut_table = [
    (
        "startmenuShortcutDoc",  # Shortcut
        "PMenu",  # Directory_
        "{} Documentation".format(create_msi_tablename(metadata["name"], "PyHathiPrep")),
        "TARGETDIR",  # Component_
        "[TARGETDIR]documentation.url",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        'TARGETDIR'  # WkDir
    ),
]

if os.path.exists(MSVC):
    INCLUDE_FILES.append(MSVC)

build_exe_options = {
    "includes": pytest.freeze_includes(),
    "include_msvcr": True,
    "packages": [
        "os",
        'pytest',
        "packaging",
        "six",
        "appdirs",
        "pytz",
        "tzlocal",
        "pyhathiprep",
        "setuptools",
    ],
    "namespace_packages": ["ruamel.yaml"],
    "excludes": ["tkinter"],
    "include_files": INCLUDE_FILES,

}

target_name = 'pyhathiprep.exe' if platform.system() == "Windows" else 'pyhathiprep'
cx_Freeze.setup(
    name="PyHathiPrep",
    description=metadata["description"],
    license="University of Illinois/NCSA Open Source License",
    version=metadata["version"],
    author=metadata["author"],
    author_email=metadata["author_email"],
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {
            "upgrade_code": "{D08D5F4C-EF6E-4D16-939C-2C441DF88675}",
            "data": {
                "Shortcut": shortcut_table,
                "Directory": directory_table
            },

        }
    },
    executables=[cx_Freeze.Executable("pyhathiprep/__main__.py",
                                      targetName=target_name, base="Console")],

)
