"""Generating checksum reports."""

import os
import hashlib
import abc
from collections import namedtuple
import typing

HashValue = namedtuple("HashValue", ("filename", "hash"))

CHUNK_SIZE = 2 ** 20


class AbsChecksumBuilder(metaclass=abc.ABCMeta):
    """Abstract base class for generating checksums."""

    def __init__(self) -> None:
        """Create a new builder object."""
        self._files: typing.List[HashValue] = []

    def add_entry(self, filename: str, hash_value: str) -> None:
        """Add Additional file to for a checksum to be calculated.

        Args:
            filename:
            hash_value:

        """
        self._files.append(HashValue(filename=filename, hash=hash_value))

    @abc.abstractmethod
    def build(self) -> str:
        """Construct a new report as a string."""


class HathiChecksumReport(AbsChecksumBuilder):
    """Generate a new Checksum report for Hathi."""

    @staticmethod
    def _format_entry(filename: str, hash_value: str) -> str:
        return "{} *{}".format(hash_value, filename)

    def build(self) -> str:
        """Construct a new report as a string."""
        lines = []
        for entry in sorted(self._files, key=lambda x: x.filename):

            lines.append(self._format_entry(
                filename=entry.filename, hash_value=entry.hash)
            )

        return "{}\n".format("\n".join(lines))


def calculate_md5_hash(file_path: str) -> str:
    """Calculate the md5 hash value of a file.

    Args:
        file_path: Path to a file

    Returns: Hash value as a string

    """
    if not os.path.isfile(file_path):
        raise ValueError("Not a valid file: '{}'".format(file_path))

    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b""):
            md5_hash.update(chunk)
    hash_value = md5_hash.hexdigest()
    return hash_value


def create_checksum_report(path) -> str:
    """Generate a checksum report.

    Args:
        path: Location of the files that should be included in the report

    Returns:
        New report as a string

    """
    report_builder = HathiChecksumReport()

    for file in filter(lambda x: os.path.isfile(x.path), os.scandir(path)):
        hash_value = calculate_md5_hash(file.path)
        report_builder.add_entry(file.name, hash_value)
    return report_builder.build()
