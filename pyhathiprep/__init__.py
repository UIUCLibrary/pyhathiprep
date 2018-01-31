import os
import sys

from .hathiyml import make_yml
from setuptools.config import read_configuration
from pkg_resources import get_distribution, DistributionNotFound

FULL_TITLE = "PyHathiPrep"


def get_project_metadata(config_file):
    return read_configuration(config_file)["metadata"]


def get_version():
    try:
        package_metadata = get_distribution("pyhathiprep")
        version = package_metadata.version
    except DistributionNotFound as e:

        # =====================================================================
        # In the case of CX_FREEZE. As of version 5.1.1, it doesn't build
        # package metadata files. For this reason setup.cfg must be manually
        # included as part of the setup script, which it includes it to the
        # same path as the main exe.
        # =====================================================================
        setup_cfg = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", "setup.cfg"))
        if os.path.exists(setup_cfg):
            metadata = get_project_metadata(setup_cfg)
            if metadata["name"] == "pyhathiprep":
                return metadata["version"]
        # =====================================================================

        print("Has the metadata for this project been built?", file=sys.stderr)
        version = "Unknown"
    except FileNotFoundError as e:
        version = "Unknown"
    return version


__version__ = get_version()
