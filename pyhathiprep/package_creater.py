"""Module for the creation of packages."""

import os
import shutil
import tempfile
import abc
import typing
from datetime import datetime
import logging
import warnings
from pyhathiprep import make_yml
from pyhathiprep.utils import derive_package_prefix
from pyhathiprep.checksum import create_checksum_report

MOVING_LOG_MESSAGE = "Moving %s to %s"


class AbsPackageCreator(metaclass=abc.ABCMeta):
    """Base class for creating packages."""

    def __init__(self, source: str) -> None:
        """Create a new package.

        Args:
            source:
        """
        self._source = source
        self._prefix = derive_package_prefix(source)

    @abc.abstractmethod
    def create_checksum_report(self, build_path):
        """Create a checksum report.

        Args:
            build_path:

        """

    @staticmethod
    def generate_checksum_report(
            source_path: str,
            destination_path: str,
    ):
        """Generate checksum report.

        Args:
            source_path: Path to files used in checksum report.
            destination_path: Output file path the save the report.

        """
        logger = logging.getLogger(__name__)
        logger.debug("Making checksum.md5 for %s", source_path)
        checksum_report = create_checksum_report(source_path)
        with open(
                os.path.join(destination_path, "checksum.md5"),
                "w",
                encoding="utf-8"
        ) as write_file:
            write_file.write(checksum_report)

    @staticmethod
    def generate_meta_yaml(
            source_path: str,
            destination_path: str,
            title_page: typing.Optional[str]
    ):
        """Generate meta.yaml file.

        Args:
            source_path: path to find files
            destination_path: path to the location to write the file
            title_page: title page for the package

        """
        logger = logging.getLogger(__name__)
        logger.debug("Making YAML for %s", destination_path)
        yml = make_yml(
            source_path, capture_date=datetime.now(), title_page=title_page
        )
        with open(
                os.path.join(destination_path, "meta.yml"),
                "w",
                encoding="utf-8"
        ) as write_file:
            write_file.write(yml)

    @abc.abstractmethod
    def make_yaml(self, build_path, title_page=None):
        """Create a yml file.

        Args:
            build_path:
            title_page:

        """

    def copy_source(self, build_path):
        """Copy the source.

        Args:
            build_path:

        """

    @abc.abstractmethod
    def deploy(self, build_path, destination, overwrite=False):
        """Put the files somewhere.

        Args:
            build_path:
            destination:
            overwrite:

        """

    def generate_package(self, destination=None, overwrite=False,
                         title_page=None):
        """Generate a new package.

        Args:
            destination:
            overwrite:
            title_page:

        """
        with tempfile.TemporaryDirectory() as temp:
            self.copy_source(build_path=temp)
            self.make_yaml(build_path=temp, title_page=title_page)
            self.create_checksum_report(build_path=temp)

            self.deploy(
                build_path=temp, destination=destination, overwrite=overwrite
            )


class InplacePackage(AbsPackageCreator):
    """Build package inplace."""

    def make_yaml(self, build_path, title_page=None):
        """Create a yml file.

        Args:
            build_path:
            title_page:

        """
        self.generate_meta_yaml(self._source, build_path, title_page)

    def create_checksum_report(self, build_path):
        """Create a checksum report.

        Args:
            build_path:

        """
        self.generate_checksum_report(
            source_path=self._source,
            destination_path=build_path
        )

    def deploy(self, build_path, destination=None, overwrite=False):
        """Put the files somewhere.

        Args:
            build_path:
            destination:
            overwrite:

        """
        logger = logging.getLogger(__name__)
        for item in os.scandir(build_path):
            save_dest = os.path.join(self._source, item.name)
            if os.path.exists(save_dest):
                if overwrite:
                    os.remove(save_dest)
            logger.debug(MOVING_LOG_MESSAGE, item.path, save_dest)
            shutil.move(item.path, save_dest)


class NewPackage(AbsPackageCreator):
    """Generating a new packages."""

    def make_yaml(self, build_path, title_page=None):
        """Create a yml file.

        Args:
            build_path:
            title_page:

        """
        self.generate_meta_yaml(build_path, build_path, title_page)

    def create_checksum_report(self, build_path):
        """Create a checksum report.

        Args:
            build_path:

        """
        self.generate_checksum_report(
            source_path=build_path,
            destination_path=build_path
        )

    def copy_source(self, build_path):
        """Copy the source.

        Args:
            build_path:

        """
        logger = logging.getLogger(__name__)
        for item in filter(lambda x: x.is_file(), os.scandir(self._source)):
            logger.debug("Copying %s to %s", item.path, build_path)
            # logger.debug("Copying {} to {}".format(item.path, build_path))
            shutil.copyfile(item.path, os.path.join(build_path, item.name))

    def deploy(self, build_path, destination=None, overwrite=False):
        """Put the files somewhere.

        Args:
            build_path:
            destination:
            overwrite:

        """
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
                    "Cannot create destination folder because it already"
                    " exists: '{}'.".format(new_package_path))

        os.makedirs(new_package_path)

        for item in os.scandir(build_path):
            logger.debug(MOVING_LOG_MESSAGE, item.path, new_package_path)
            shutil.move(item.path, new_package_path)


def create_package(source: str, destination=None, prefix=None,
                   overwrite=False) -> None:
    """Create a single package folder for Hathi.

    Args:
        source: Path to source files
        destination: Path where the package will be saved after prepped
        prefix: the name of the directory that the package will be saved in.
            If none given, it will use the name of the parent directory
        overwrite: If destination already exists, remove first it before
            saving.

    """
    if destination:
        new_creator = NewPackage(source)
        new_creator.generate_package(destination, overwrite=overwrite)
    else:
        inplace_creator = InplacePackage(source)
        inplace_creator.generate_package(overwrite=overwrite)


def create_new_package(source, destination, prefix=None, overwrite=False,
                       title_page=None):
    """Create a new package.

    Args:
        source:
        destination:
        prefix:
        overwrite:
        title_page:

    """
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
                "Cannot create destination folder because it already "
                "exists: '{}'.".format(new_package_path))

    with tempfile.TemporaryDirectory() as temp:
        # Copy contents to temp folder
        for item in filter(lambda x: x.is_file(), os.scandir(source)):
            logger.debug("Copying %s to %s", item.path, temp)
            shutil.copyfile(item.path, os.path.join(temp, item.name))

        # make YML and checksum
        AbsPackageCreator.generate_meta_yaml(temp, temp, title_page)
        AbsPackageCreator.generate_checksum_report(temp, temp)

        # On success move everything to destination
        os.makedirs(new_package_path)
        for item in os.scandir(temp):
            logger.debug(MOVING_LOG_MESSAGE, item.path, new_package_path)
            shutil.move(item.path, new_package_path)
