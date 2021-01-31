"""Utility functions."""

import os
import typing


def get_packages(root) -> typing.Iterator[str]:
    """Find packages at a given root.

    Args:
        root: Root directory of the packages

    Yields:
        Path to package

    """
    for item in filter(lambda x: x.is_dir(), os.scandir(root)):
        yield item.path


def derive_package_prefix(path):
    """Derive a package prefix name based on path given.

    Args:
        path:

    Returns:
        Prefix

    Examples:

    .. testsetup::

        from pyhathiprep.utils import derive_package_prefix

    .. doctest::

        >>> derive_package_prefix("hborcher/temp/DSHTPrep_Test/7213857")
        '7213857'

    """
    return os.path.normpath(path).split(os.path.sep)[-1]
