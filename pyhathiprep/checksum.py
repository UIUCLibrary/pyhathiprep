import os
import hashlib
import abc
from collections import namedtuple
import typing

HashValue = namedtuple("HashValue", ("filename", "hash"))

CHUNK_SIZE = 2 ** 20


class AbsChecksumBuilder(metaclass=abc.ABCMeta):
    def __init__(self) -> None:

        self._files = []  # type: typing.List[HashValue]

    def add_entry(self, filename: str, hash_value: str) -> None:
        self._files.append(HashValue(filename=filename, hash=hash_value))

    @abc.abstractmethod
    def build(self) -> str:
        pass


class HathiChecksumReport(AbsChecksumBuilder):
    @staticmethod
    def _format_entry(filename: str, hash_value: str) -> str:
        return "{} *{}".format(hash_value, filename)

    def build(self) -> str:
        lines = []
        for entry in sorted(self._files, key=lambda x: x.filename):
            lines.append(self._format_entry(filename=entry.filename, hash_value=entry.hash))

        return "{}\n".format("\n".join(lines))


def calculate_md5_hash(file_path: str) -> str:
    """Calculate the md5 hash value of a file

    Args:
        file_path: Path to a file

    Returns: Hash value as a string

    """
    if not os.path.isfile(file_path):
        raise ValueError("Not a valid file: '{}'".format(file_path))

    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            md5_hash.update(chunk)
    hash_value = md5_hash.hexdigest()
    return hash_value


def create_checksum_report(path) -> str:
    report_builder = HathiChecksumReport()

    for f in filter(lambda x: os.path.isfile(x.path), os.scandir(path)):
        hash_value = calculate_md5_hash(f.path)
        report_builder.add_entry(f.name, hash_value)
    return report_builder.build()
