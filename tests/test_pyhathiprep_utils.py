import os
import shutil

import pytest

import pyhathiprep.package_creater
from pyhathiprep import utils

PACKAGE_NAME = "7213857"
SOURCE_FILES = [
    "00000001.jp2", "00000001.txt",
    "00000002.jp2", "00000002.txt",
    "00000003.jp2", "00000003.txt",
    "00000004.jp2", "00000004.txt",
    "00000005.jp2", "00000005.txt",
    "00000006.jp2", "00000006.txt",
    "00000007.jp2", "00000007.txt",
    "00000008.jp2", "00000008.txt",
    "00000009.jp2", "00000009.txt",
    "00000010.jp2", "00000010.txt",
    "00000011.jp2", "00000011.txt",
    "00000012.jp2", "00000012.txt",
    "00000013.jp2", "00000013.txt",
    "00000014.jp2", "00000014.txt",
    "00000015.jp2", "00000015.txt",
    "00000016.jp2", "00000016.txt",
    "00000017.jp2", "00000017.txt",
    "00000018.jp2", "00000018.txt",
    "marc.xml",
]


@pytest.fixture(scope="session")
def package_source_fixture(tmpdir_factory):

    new_package = tmpdir_factory.mktemp(PACKAGE_NAME, numbered=False)
    for file in SOURCE_FILES:
        new_file = new_package.join(file)
        print("Creating test file {}".format(new_file))
        with open(new_file, "w") as w:
            pass
    return new_package


def test_derive_package_prefix():
    source = os.path.join("hborcher", "temp", "DSHTPrep_Test", PACKAGE_NAME)
    prefix = utils.derive_package_prefix(source)
    assert prefix == PACKAGE_NAME


def test_create_package(package_source_fixture, tmpdir):
    print("package_source_fixture = {}".format(str(package_source_fixture)))
    destination = tmpdir.mkdir("test_dest")
    pyhathiprep.package_creater.create_package(source=str(package_source_fixture), destination=str(destination))
    new_created_package = os.path.join(str(destination), PACKAGE_NAME)
    print("Checking to see if {} exists".format(new_created_package))
    assert os.path.exists(new_created_package)
    for original_file in SOURCE_FILES:
        expected_copied_file = os.path.join(new_created_package, original_file)
        print("Checking for {}".format(expected_copied_file))
        assert os.path.exists(expected_copied_file)

    yml_file = os.path.join(new_created_package, "meta.yml")
    print("Checking for {}".format(yml_file))
    assert os.path.exists(yml_file)

    checksum = os.path.join(new_created_package, "checksum.md5")
    print("Checking for {}".format(checksum))
    assert os.path.exists(checksum)
