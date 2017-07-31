import os

import pytest

from pyhathiprep import utils

PACKAGE_NAME = "7213857"

def test_derive_package_prefix():
    source = os.path.join("hborcher", "temp", "DSHTPrep_Test", PACKAGE_NAME)
    prefix = utils.derive_package_prefix(source)
    assert prefix == PACKAGE_NAME


