"""Executable package."""

import sys

from pyhathiprep import cli


def main(args=None, test_suite=None):
    """Launch CLI application.

    Note: If pytest is embedded with the test files, the module can test itself

    Args:
        args: Optional system args, else taken from the cli args
        test_suite:

    """
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
            print(f"Unable to run tests. Reason {error}",
                  file=sys.stderr)
            sys.exit(1)
    else:
        cli.main()


if __name__ == '__main__':
    main()
