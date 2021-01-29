import sys

from pyhathiprep import cli


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        try:
            import pytest  # type: ignore
            sys.exit(pytest.main(sys.argv[2:]))
        except ImportError as error:
            print("Unable to run tests. Reason {}".format(error), file=sys.stderr)
            sys.exit(1)
    else:
        cli.main()


if __name__ == '__main__':
    main()
