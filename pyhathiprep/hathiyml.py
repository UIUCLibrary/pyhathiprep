import os
import io
import abc
import typing
from datetime import datetime
import ruamel.yaml  # type: ignore
import tzlocal  # type: ignore


class AbsYmlBuilder(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = dict()
        self._page_data = dict()
        for k, v in self.boilerplate().items():
            self.data[k] = v

    def add_pagedata(self, filename, **attributes) -> None:
        if filename in self._page_data:
            raise KeyError("{} Already exists".format(filename))
        else:
            self._page_data[filename] = attributes

    @abc.abstractmethod
    def boilerplate(self) -> typing.Dict[str, str]:
        """
        Set static items.
        """
        pass

    @abc.abstractmethod
    def build(self):
        pass


class HathiYmlBuilder(AbsYmlBuilder):

    def boilerplate(self) -> typing.Dict[str, str]:
        return {
            "capture_agent": "IU",
            "scanner_user": "University of Illinois Digital Content Creation Unit"
        }

    def set_data(self, key, value):
        self.data[key] = value

    def set_capture_date(self, date: datetime):
        tz = tzlocal.get_localzone()
        if date.tzinfo is None:
            capture_date = tz.localize(date)
        else:
            capture_date = date
        self.data["capture_date"] = capture_date.isoformat(timespec="minutes")

    def build(self):
        ordered = [
            "capture_date",
            "capture_agent",
            "scanner_user"

        ]

        yml = ruamel.yaml.YAML()
        yml.indent = 4
        yml.default_flow_style = False

        data = dict()

        # Put the items require an order to them first
        for key in ordered:
            if self.data[key]:
                data[key] = self.data[key]

        # Then anything else
        for key, value in filter(lambda i: i[0] not in ordered, self.data.items()):
            data[key] = value

        # Finally add the pages
        data["pagedata"] = self._page_data

        # Render the dict as yml formatted string
        with io.StringIO() as yml_string_writer:
            yml.dump(data, yml_string_writer)
            yml_string_writer.seek(0)
            yml_str = yml_string_writer.read()
        return yml_str


def make_yml(directory: str, title_page=None, **overrides) -> str:
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
        attribute = dict()
        relative_path = os.path.relpath(image, directory)
        if relative_path == title_page:
            attribute["label"] = "TITLE"
        builder.add_pagedata(relative_path, **attribute)
    return builder.build()


def get_images(directory, page_data_extensions=(".jp2", ".tif")):
    for root, dirs, files in os.walk(directory):
        for file_ in files:
            if os.path.splitext(file_)[1] in page_data_extensions:
                yield os.path.join(root, file_)
