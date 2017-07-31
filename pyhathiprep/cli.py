import pyhathiprep
from pyhathiprep.package_creater import create_package
from pyhathiprep.utils import get_packages
from . import configure_logging
import argparse
import os


def destination_path(path):
    if not os.path.exists(path):
        raise ValueError("{} is an invalid path".format(path))

    if not os.path.isdir(path):
        raise ValueError("{} is not a path".format(path))

    return os.path.abspath(path)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=pyhathiprep.__description__)

    parser.add_argument(
        '--version',
        action='version',
        version=pyhathiprep.__version__
    )

    parser.add_argument(
        "source",
        help="Path to the source directory of files that need to be prepped"
    )
    parser.add_argument(
        "dest",
        type=destination_path,
        help="Path to save new hathi prep."
    )

    parser.add_argument(
        "-o", "--overwrite",
        action="store_true",
        help="Overwrite any existing files and folders"
    )
    # parser.add_argument(
    #     "--remove",
    #     action="store_true",
    #     help="Remove original files after successfully preped"
    # )

    debug_group = parser.add_argument_group("Debug")

    debug_group.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")
    debug_group.add_argument("--log-debug", dest="log_debug", help="Save debug information to a file")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    logger = configure_logging.configure_logger(debug_mode=args.debug, log_file=args.log_debug)
    logger.info("Prepping folder in {}".format(args.source))
    for package in get_packages(args.source):
        logger.info("    {}".format(package))
        try:
            create_package(source=package, destination=args.dest, overwrite=args.overwrite)
        except FileExistsError as e:
            print(e)
