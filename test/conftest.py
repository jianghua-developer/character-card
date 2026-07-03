import pytest
import sys
from pathlib import Path
from typer.testing import CliRunner

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

runner = CliRunner()


@pytest.fixture(scope="session")
def cli_runner():
    return runner


@pytest.fixture
def mock_confirm(monkeypatch):
    monkeypatch.setattr("typer.confirm", lambda *args, **kwargs: True)


@pytest.fixture
def test_csv_path():
    from pathlib import Path

    return Path(__file__).parent / "fixtures" / "test_config.csv"
