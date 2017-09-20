import os
import shutil
import tempfile
import abc
from datetime import datetime
import logging
from pyhathiprep import make_yml
from pyhathiprep.utils import derive_package_prefix
from pyhathiprep.checksum import create_checksum_report
import warnings


class AbsPackageCreator(metaclass=abc.ABCMeta):
    def __init__(self, source: str) -> None:
        self._source = source
        self._prefix = derive_package_prefix(source)

    @abc.abstractmethod
    def create_checksum_report(self, build_path):
        pass

    @abc.abstractmethod
    def make_yaml(self, build_path):
        pass

    def copy_source(self, build_path):
        pass

    @abc.abstractmethod
    def deploy(self, build_path, destination, overwrite=False):
        pass

    def generate_package(self, destination=None, overwrite=False):
        with tempfile.TemporaryDirectory() as temp:
            self.copy_source(build_path=temp)
            self.make_yaml(build_path=temp)
            self.create_checksum_report(build_path=temp)
            self.deploy(build_path=temp, destination=destination, overwrite=overwrite)


class InplacePackage(AbsPackageCreator):
    def make_yaml(self, build_path):
        logger = logging.getLogger(__name__)
        logger.debug("Making YAML for {}".format(build_path))
        yml = make_yml(self._source, capture_date=datetime.now())
        with open(os.path.join(build_path, "meta.yml"), "w") as w:
            w.write(yml)

    def create_checksum_report(self, build_path):
        logger = logging.getLogger(__name__)
        logger.debug("Making checksum.md5 for {}".format(build_path))
        checksum_report = create_checksum_report(self._source)
        with open(os.path.join(build_path, "checksum.md5"), "w") as w:
            w.write(checksum_report)

    def deploy(self, build_path, destination=None, overwrite=False):
        logger = logging.getLogger(__name__)
        for item in os.scandir(build_path):
            save_dest = os.path.join(self._source, item.name)
            if os.path.exists(save_dest):
                if overwrite:
                    os.remove(save_dest)
            logger.debug("Moving {} to {}".format(item.path, save_dest))
            shutil.move(item.path, save_dest)


class NewPackage(AbsPackageCreator):
    def make_yaml(self, build_path):
        logger = logging.getLogger(__name__)
        logger.debug("Making YAML for {}".format(build_path))
        yml = make_yml(build_path, capture_date=datetime.now())
        with open(os.path.join(build_path, "meta.yml"), "w") as w:
            w.write(yml)

    def create_checksum_report(self, build_path):
        logger = logging.getLogger(__name__)
        logger.debug("Making checksum.md5 for {}".format(build_path))
        checksum_report = create_checksum_report(build_path)
        with open(os.path.join(build_path, "checksum.md5"), "w") as w:
            w.write(checksum_report)

    def copy_source(self, build_path):
        logger = logging.getLogger(__name__)
        for item in filter(lambda x: x.is_file(), os.scandir(self._source)):
            logger.debug("Copying {} to {}".format(item.path, build_path))
            shutil.copyfile(item.path, os.path.join(build_path, item.name))

    def deploy(self, build_path, destination=None, overwrite=False):
        logger = logging.getLogger(__name__)
        if not destination:
            raise AttributeError("Missing destination")
        new_package_path = os.path.join(destination, self._prefix)

        if os.path.exists(new_package_path):
            if overwrite:
                # Remove destination path first
                shutil.rmtree(new_package_path)
            else:
                raise FileExistsError(
                    "Cannot create destination folder because it already exists: '{}'.".format(new_package_path))
        os.makedirs(new_package_path)

        for item in os.scandir(build_path):
            logger.debug("Moving {} to {}".format(item.path, new_package_path))
            shutil.move(item.path, new_package_path)


def create_package(source: str, destination=None, prefix=None, overwrite=False) -> None:
    """ Create a single package folder for Hathi

    Args:
        source: Path to source files
        destination: Path where the package will be saved after prepped
        prefix: the name of the directory that the package will be saved in. If none given, it will use the name of the
            parent directory
        overwrite: If destination already exists, remove first it before saving.

    """
    if destination:
        new_creator = NewPackage(source)
        new_creator.generate_package(destination, overwrite=overwrite)
    else:
        inplace_creator = InplacePackage(source)
        inplace_creator.generate_package(overwrite=overwrite)


def create_new_package(source, destination, prefix=None, overwrite=False):
    warnings.warn("Use NewPackage class instead", DeprecationWarning)
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
