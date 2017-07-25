import os
import io
import abc
from ruamel.yaml import YAML
from pytz import timezone
import typing
from datetime import datetime


class AbsYmlBuilder(metaclass=abc.ABCMeta):
    def __init__(self):
        self._page_data = dict()

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
    def __init__(self):
        super().__init__()
        self._capture_date = None

    def boilerplate(self) -> typing.Dict[str, str]:
        return {
            "capture_agent": "IU",
            "scanner_user": "University of Illinois Digital Content Creation Unit"
        }

    def set_capture_date(self, date: datetime):
        # # datetime.tzinfo = timezone("US/Central")
        # if date.tzinfo is None:
        #     date.replace(tzinfo = timezone("US/Central"))
        self._capture_date = date

    def build(self):
        yml = YAML()
        yml.default_flow_style = False
        yml.preserve_quotes = False

        data = dict()
        data["capture_date"] = self._capture_date.isoformat(timespec="seconds")
        for key, value in self.boilerplate().items():
            data[key] = value
        data["pagedata"] = self._page_data

        # Render the dict as yml formatted string
        with io.StringIO() as yml_string_writer:
            yml.dump(data, yml_string_writer)
            yml_string_writer.seek(0)
            yml_str = yml_string_writer.read()
        return yml_str



def make_yml(directory: str, output_name: str, **overrides):
    # Check if directory is a valid path

    if not os.path.isdir(directory):
        raise FileNotFoundError("Invalid directory, {}".format(directory))
    builder = HathiYmlBuilder()
    # TODO change to be dynamic in this
    builder.set_capture_date(datetime.now())

    for key, value in overrides.items():
        print(key, value)


    for image in get_images(directory):
        print(image)

    raise NotImplementedError


def get_images(directory, page_data_extensions=(".jp2", ".tif")):
    for root, dirs, files in os.walk(directory):
        for file_ in files:
            if os.path.splitext(file_)[1] in page_data_extensions:
                yield os.path.join(root, file_)
