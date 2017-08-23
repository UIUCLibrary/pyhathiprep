import itertools
import pytz
import pyhathiprep
import pytest
from pyhathiprep.hathiyml import HathiYmlBuilder
from datetime import datetime, timezone
import ruamel.yaml
import difflib
files = ["00000001.jp2", "00000002.jp2", "00000003.jp2", "00000004.jp2",
         "00000005.jp2", "00000006.jp2", "00000007.jp2", "00000008.jp2",
         "00000009.jp2", "00000010.jp2", "00000011.jp2", "00000012.jp2",
         "00000013.jp2", "00000014.jp2", "00000015.jp2", "00000016.jp2",
         "00000017.jp2", "00000018.jp2", "00000019.jp2", "00000020.jp2",
         "00000021.jp2", "00000022.jp2", "00000023.jp2", "00000024.jp2",
         "00000025.jp2", "00000026.jp2", "00000027.jp2", "00000028.jp2",
         "00000029.jp2", "00000030.jp2", "00000031.jp2", "00000032.jp2",
         "00000033.jp2", "00000034.jp2", "00000035.jp2", "00000036.jp2",
         "00000037.jp2", "00000038.jp2", "00000039.jp2", "00000040.jp2",
         "00000041.jp2", "00000042.jp2", "00000043.jp2", "00000044.jp2",
         "00000045.jp2", "00000046.jp2", "00000047.jp2", "00000048.jp2",
         "00000049.jp2", "00000050.jp2", "00000051.jp2", "00000052.jp2",
         "00000053.jp2", "00000054.jp2", "00000055.jp2", "00000056.jp2",
         ]


class TestMakeYAML:
    @pytest.fixture(scope="session")
    def dummy_fixture(self, tmpdir_factory):
        x = tmpdir_factory.mktemp("2693684")
        for f in files:
            with open(x.join(f), "w"):
                pass

        return x

    def test_make_yml(self, dummy_fixture):
        tz = pytz.timezone("America/Chicago")
        test_date = tz.localize(datetime(year=2017, month=7, day=3, hour=14, minute=22, second=0))
        yml = pyhathiprep.make_yml(dummy_fixture, capture_date=test_date, scanner_user="Henry")
        yml_parser = ruamel.yaml.YAML()
        parsed = yml_parser.load(yml)
        assert parsed["scanner_user"] == "Henry"
        for expected_page_name, (actual_page_name, actual_page_values) in zip(files, parsed["pagedata"].items()):
            assert expected_page_name == actual_page_name

    def test_make_yml_with_title(self, dummy_fixture):
        tz = pytz.timezone("America/Chicago")
        test_date = tz.localize(datetime(year=2017, month=7, day=3, hour=14, minute=22))
        yml = pyhathiprep.make_yml(dummy_fixture, title_page="00000033.jp2", capture_date=test_date,
                                   scanner_user="Henry")

        yml_parser = ruamel.yaml.YAML()
        parsed = yml_parser.load(yml)
        assert parsed["scanner_user"] == "Henry"
        for expected_page_name, (actual_page_name, actual_page_values) in zip(files, parsed["pagedata"].items()):
            assert expected_page_name == actual_page_name
            if actual_page_name == "00000033.jp2":
                assert actual_page_values["label"] == "TITLE"


def test_hathi_yml_builder():
    expected_yml = """capture_date: 2017-07-03T14:22:00-05:00
capture_agent: IU
scanner_user: University of Illinois Digitization Services
pagedata:
    00000001.jp2: {}
    00000002.jp2: {}
    00000003.jp2:
        label: TITLE
    00000004.jp2: {}
    00000005.jp2: {}
"""

    builder = HathiYmlBuilder()
    for file in ["00000001.jp2", "00000002.jp2", "00000003.jp2", "00000004.jp2", "00000005.jp2"]:
        if file == "00000003.jp2":
            builder.add_pagedata(file, label="TITLE")
        else:
            builder.add_pagedata(file)
    tz = pytz.timezone("America/Chicago")
    builder.set_capture_date(

        tz.localize(datetime(year=2017, month=7, day=3, hour=14, minute=22, second=0))
    )
    yml = builder.build()

    diff = difflib.unified_diff(yml.splitlines(keepends=True), expected_yml.splitlines(keepends=True))
    errors = []
    for error in diff:
        if not error.startswith(" "):
            errors.append(error)
            # print(x)
        # else:
    if errors:
        pytest.fail("".join(errors))

