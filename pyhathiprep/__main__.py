import sys

from pyhathiprep import cli


def main(args=None, test_suite=None):
    args = args or sys.argv
    if len(args) > 1 and args[1] == "--pytest":
        try:
            if test_suite is None:
                def test_suite():
                    # pylint: disable=import-outside-toplevel
                    import pytest  # type: ignore
                    return pytest.main(args)
            sys.exit(test_suite())
        except ImportError as error:
            print("Unable to run tests. Reason {}".format(error),
                  file=sys.stderr)
            sys.exit(1)
    else:
        cli.main()


if __name__ == '__main__':
    main()
