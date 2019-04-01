import os
import shutil

from pyhathiprep import checksum
import pytest

PACKAGE_NAME = "7213856"
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
    "meta.yml"
]

expected_report = """f1b708bba17f1ce948dc979f4d7092bc *00000001.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000001.txt
f1b708bba17f1ce948dc979f4d7092bc *00000002.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000002.txt
f1b708bba17f1ce948dc979f4d7092bc *00000003.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000003.txt
f1b708bba17f1ce948dc979f4d7092bc *00000004.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000004.txt
f1b708bba17f1ce948dc979f4d7092bc *00000005.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000005.txt
f1b708bba17f1ce948dc979f4d7092bc *00000006.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000006.txt
f1b708bba17f1ce948dc979f4d7092bc *00000007.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000007.txt
f1b708bba17f1ce948dc979f4d7092bc *00000008.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000008.txt
f1b708bba17f1ce948dc979f4d7092bc *00000009.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000009.txt
f1b708bba17f1ce948dc979f4d7092bc *00000010.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000010.txt
f1b708bba17f1ce948dc979f4d7092bc *00000011.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000011.txt
f1b708bba17f1ce948dc979f4d7092bc *00000012.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000012.txt
f1b708bba17f1ce948dc979f4d7092bc *00000013.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000013.txt
f1b708bba17f1ce948dc979f4d7092bc *00000014.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000014.txt
f1b708bba17f1ce948dc979f4d7092bc *00000015.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000015.txt
f1b708bba17f1ce948dc979f4d7092bc *00000016.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000016.txt
f1b708bba17f1ce948dc979f4d7092bc *00000017.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000017.txt
f1b708bba17f1ce948dc979f4d7092bc *00000018.jp2
f1b708bba17f1ce948dc979f4d7092bc *00000018.txt
f1b708bba17f1ce948dc979f4d7092bc *marc.xml
f1b708bba17f1ce948dc979f4d7092bc *meta.yml
"""


@pytest.fixture(scope="session")
def package_source_fixture_b(tmpdir_factory):
    new_package = tmpdir_factory.mktemp(PACKAGE_NAME, numbered=False)
    for file in SOURCE_FILES:
        new_file = new_package.join(file)
        print("Creating test file {}".format(new_file))
        with open(new_file, "w") as w:
            w.write("0000000000")
    yield new_package
    shutil.rmtree(new_package)


class TestChecksums:
    def test_create_checksum(self, tmpdir_factory):
        data = b"0000000000"
        temp_dir = tmpdir_factory.mktemp("testchecksum", numbered=False)
        # temp_dir = tmpdir.mkdir("testchecksum")
        test_file = os.path.join(temp_dir, "dummy.txt")
        with open(test_file, "wb") as w:
            w.write(data)
            # test_file.write(data)
        expected_hash = "f1b708bba17f1ce948dc979f4d7092bc"
        assert expected_hash == checksum.calculate_md5_hash(test_file)
        shutil.rmtree(temp_dir)


    def test_generate_report(self, package_source_fixture_b):
        expected_report_lines = expected_report.split("\n")
        report = checksum.create_checksum_report(package_source_fixture_b)
        report_lines = report.split("\n")
        for expected_line, actual_line in zip(report.split("\n"), expected_report.split("\n")):
            assert expected_line == actual_line
        # assert checksum.create_checksum_report(package_source_fixture_b) == expected_report
