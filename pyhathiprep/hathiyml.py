"""Generating YAML data."""

import os
import io
import abc
import functools
import typing
from typing import Dict
from datetime import datetime
import ruamel.yaml
import tzlocal

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec  # type: ignore


class AbsYmlBuilder(metaclass=abc.ABCMeta):
    """Abstract base class for creating YML builders."""

    def __init__(self):
        """Create a builder yaml class."""
        self.data = {}
        self._page_data = {}
        for key, value in self.boilerplate().items():
            self.data[key] = str(value)

    def add_pagedata(self, filename: str, **attributes) -> None:
        """Add pagedata.

        Args:
            filename:
            **attributes:

        """
        if filename in self._page_data:
            raise KeyError(f"{filename} Already exists")
        self._page_data[filename] = attributes

    @abc.abstractmethod
    def boilerplate(self) -> Dict[str, str]:
        """Get standard data.

        Returns:
            Dictionary of prefilled data

        """

    @abc.abstractmethod
    def build(self) -> str:
        """Construct the YAML data.

        Returns:
            YAML data as a string.
        """


Param = ParamSpec("Param")


def strip_date_quotes(
        func: typing.Callable[Param, str]
) -> typing.Callable[Param, str]:
    """Remove quotes added around dates.

    This is a hack, that's required right now because ruamel.yaml seems to
        inconsistent about its date formatting.

    Args:
        func:

    Returns: YAML formatted string

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        yml_data = func(*args, **kwargs)
        cleaned_lines = []
        for line in yml_data.splitlines(keepends=True):
            if "capture_date" in line:
                key, value = line.split(": ")
                new_value = value.strip("\n").strip("'")
                new_line = "{}: {}\n".format(key, new_value)
                cleaned_lines.append(new_line)
            else:
                cleaned_lines.append(line)

        return "".join(cleaned_lines)

    return wrapper


class HathiYmlBuilder(AbsYmlBuilder):
    """Builder for YML data."""

    def boilerplate(self) -> Dict[str, str]:
        """Get standard data.

        Returns:
            Dictionary of prefilled data

        """
        return {
            "capture_agent": "illinois",
            "scanner_user": "University of Illinois Digitization Services"
        }

    def set_data(self, key, value):
        """Set the data value.

        Args:
            key:
            value:

        """
        self.data[key] = value

    def set_capture_date(self, date: datetime) -> None:
        """Set the capture date.

        Args:
            date:

        """
        timezone = tzlocal.get_localzone()
        if date.tzinfo is None:
            capture_date = timezone.localize(date)
        else:
            capture_date = date
        self.data["capture_date"] = capture_date.isoformat(timespec="seconds")

    @strip_date_quotes
    def build(self) -> str:
        """Construct the YAML data.

        Returns:
            YAML data as a string.

        """
        ordered = [
            "capture_date",
            "capture_agent",
            "scanner_user"

        ]

        yml = ruamel.yaml.YAML()
        yml.indent = 4
        yml.default_flow_style = False

        data = {}

        # Put the items require an order to them first
        for key in ordered:
            if self.data[key]:
                data[key] = self.data[key]

        # Then anything else
        for key, value in filter(
                lambda i: i[0] not in ordered, self.data.items()):
            data[key] = value

        # Finally add the pages
        data["pagedata"] = self._page_data

        # Render the dict as yml formatted string
        with io.StringIO() as yml_string_writer:
            yml.dump(data, yml_string_writer)
            yml_string_writer.seek(0)
            yml_str = yml_string_writer.read()

        return yml_str


def make_yml(
        directory: str,
        title_page: typing.Optional[str] = None,
        **overrides
) -> str:
    """
    Create the data for HathiTrust YAML file from a given directory.

    Args:
        directory: Path to the HathiTrust Package
        title_page: Optional, the file name of a title page.
        **overrides: key and value of any additional variations.

    Returns: YAML formatted data.

    """
    # Check if directory is a valid path

    if not os.path.isdir(directory):
        raise FileNotFoundError("Invalid directory, {}".format(directory))

    builder = HathiYmlBuilder()

    for key, value in overrides.items():
        if key == "capture_date":
            builder.set_capture_date(value)
        else:
            builder.set_data(key, value)

    for image in get_images(directory):
        attribute = {}
        relative_path = os.path.relpath(image, directory)
        if relative_path == title_page:
            attribute["label"] = "TITLE"
        builder.add_pagedata(relative_path, **attribute)
    return builder.build()


def get_images(
        directory: str,
        page_data_extensions=(".jp2", ".tif")
) -> typing.Iterator[str]:
    """Locate image files at a location.

    Args:
        directory:
        page_data_extensions:

    Yields:
        File paths to images

    """
    for root, _, files in os.walk(directory):
        for file_ in sorted(files):
            if os.path.splitext(file_)[1] in page_data_extensions:
                yield os.path.join(root, file_)
