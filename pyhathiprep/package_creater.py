import os
import shutil
import tempfile
from datetime import datetime

from pyhathiprep import make_yml
from pyhathiprep.utils import derive_package_prefix


def create_package(source, destination, prefix=None):
    if not prefix:
        prefix = derive_package_prefix(source)

    new_package_path = os.path.join(destination, prefix)
    with tempfile.TemporaryDirectory() as temp:
        # Copy contents to temp folder
        for item in filter(lambda x: x.is_file(), os.scandir(source)):
            print("Copying {}".format(item.path))
            shutil.copyfile(item.path, os.path.join(temp, item.name))

        # make YML
        print("Making YAML for {}".format(temp))
        yml = make_yml(temp, capture_date=datetime.now(), scanner_user="Henry")
        with open(os.path.join(temp, "meta.yml"), "w") as w:
            w.write(yml)

        # On success move everything to destination
        os.makedirs(new_package_path)
        for item in os.scandir(temp):
            print("moving {} to {}".format(item.path, new_package_path))
            shutil.move(item.path, new_package_path)