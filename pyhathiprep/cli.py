from pyhathiprep.package_creater import create_package
from pyhathiprep.utils import get_packages

TEST_PATH = r"T:\HenryTest-PSR_2\DCC\DSHTPrep_Test"
DST_PATH = r"C:\Users\hborcher\temp\DSHTPrep_Test"


def main():
    print("Using TEST {}".format(TEST_PATH))
    for package in get_packages(TEST_PATH):
        print(package)
        create_package(source=package, destination=DST_PATH)
