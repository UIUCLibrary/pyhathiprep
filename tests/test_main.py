from unittest.mock import Mock, MagicMock
import sys
import pyhathiprep.__main__
from pyhathiprep import cli


def test_pytest_called_with_args(monkeypatch):
    mock_exit = Mock()
    monkeypatch.setattr(sys, "exit", mock_exit)
    mock_test_suite = Mock(return_value=0)
    pyhathiprep.__main__.main(args=[None, "--pytest"], test_suite=mock_test_suite)
    assert mock_test_suite.called is True


def test_main_calls_main_cli(monkeypatch):
    m = Mock()
    monkeypatch.setattr(cli, "main", m)
    pyhathiprep.__main__.main()
    assert m.called is True
