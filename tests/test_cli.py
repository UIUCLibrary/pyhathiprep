import argparse
from unittest.mock import Mock

from pyhathiprep import cli, configure_logging


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
