import argparse
import os
from unittest.mock import Mock, MagicMock

import pyhathiprep.utils
from pyhathiprep import cli, configure_logging, package_creater


def test_version_exits_after_being_called(monkeypatch):

    parser = cli.get_parser()
    version_exit_mock = Mock()

    with monkeypatch.context() as m:
        m.setattr(argparse.ArgumentParser, "exit", version_exit_mock)
        parser.parse_args(["--version"])

    version_exit_mock.assert_called()


def test_main_cli_reports_search_path(tmpdir, monkeypatch):
    sample_dir = tmpdir / "sample_dir"
    sample_dir.ensure_dir()
    args = argparse.Namespace()
    args.debug = False
    args.log_debug = False
    args.source = sample_dir.strpath
    mock_logger = Mock()

    def mock_configure_logger(debug_mode=False, log_file=None):
        return mock_logger

    monkeypatch.setattr(
        configure_logging, "configure_logger", mock_configure_logger
    )

    cli.main(args)
    prepping_folder_log_message = mock_logger.method_calls[0]

    # Make sure that the path searched for is passed to the logger
    assert sample_dir.strpath in prepping_folder_log_message[1][1]


def test_create_packages_called(tmpdir, monkeypatch):
    dummy_package = os.path.join(".", "dummy")
    dummy_output = os.path.join(".", "dummy_output")

    def mock_get_packages(*args, **kwargs):
        return [
            dummy_package
        ]

    mock_create_package = MagicMock()
    monkeypatch.setattr(cli, "create_package", mock_create_package)
    monkeypatch.setattr(cli, "get_packages", mock_get_packages)
    monkeypatch.setattr(cli, "destination_path", lambda x: x)

    cli.main([".", "--dest", dummy_output])

    mock_create_package.assert_called_with(
        source=dummy_package,
        destination=dummy_output,
        overwrite=False
    )
