from typer.testing import CliRunner
from json_parser.main import app
import pytest
from pathlib import Path

_TEST_ROOT = Path(__file__).parent.resolve()

@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()

def test_invalid_content(runner):
    res = runner.invoke(app, ["test/inputs/invalidcontent.json"]) 
    assert res.exit_code == 1

def test_invalid_ext(runner):
    res = runner.invoke(app, ["test/inputs/invalidext.txt"]) 
    assert res.exit_code == 2

def test_nonexistent(runner):
    res = runner.invoke(app, ["nonexistent"]) 
    assert res.exit_code == 2


def test_strstr(runner):
    res = runner.invoke(app, ["test/inputs/strstr.json"]) 
    assert res.exit_code == 0
