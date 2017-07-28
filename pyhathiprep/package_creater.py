import os
import shutil
import tempfile
from datetime import datetime
import logging
from pyhathiprep import make_yml
from pyhathiprep.utils import derive_package_prefix
from pyhathiprep.checksum import create_checksum_report


def create_package(source: str, destination: str, prefix=None, overwrite=False) -> None:
    """ Create a single package folder for Hathi

    Args:
        source: Path to source files
        destination: Path where the package will be saved after prepped
        prefix: the name of the directory that the package will be saved in. If none given, it will use the name of the
            parent directory
        overwrite: If destination already exists, remove first it before saving.

    """
    logger = logging.getLogger(__name__)
    if not prefix:
        prefix = derive_package_prefix(source)

    new_package_path = os.path.join(destination, prefix)

    if os.path.exists(new_package_path):
        if overwrite:
            # Remove destination path first
            shutil.rmtree(new_package_path)
        else:
            raise FileExistsError(
                "Cannot create destination folder because it already exists: '{}'.".format(new_package_path))
    with tempfile.TemporaryDirectory() as temp:
        # Copy contents to temp folder
        for item in filter(lambda x: x.is_file(), os.scandir(source)):
            logger.debug("Copying {} to {}".format(item.path, temp))
            shutil.copyfile(item.path, os.path.join(temp, item.name))

        # make YML
        logger.debug("Making YAML for {}".format(temp))
        yml = make_yml(temp, capture_date=datetime.now())
        with open(os.path.join(temp, "meta.yml"), "w") as w:
            w.write(yml)

        logger.debug("Making checksum.md5 for {}".format(temp))
        checksum_report = create_checksum_report(temp)
        with open(os.path.join(temp, "checksum.md5"), "w") as w:
            w.write(checksum_report)

        # On success move everything to destination
        os.makedirs(new_package_path)
        for item in os.scandir(temp):
            logger.debug("Moving {} to {}".format(item.path, new_package_path))
            shutil.move(item.path, new_package_path)
