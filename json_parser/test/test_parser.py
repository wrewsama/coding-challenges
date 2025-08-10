from typer.testing import CliRunner
from json_parser.main import app
import pytest

@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()

def test_invalid_content(runner):
    res = runner.invoke(app, ["inputs/invalidcontent.json"]) 
    assert res.exit_code == 1

def test_invalid_ext(runner):
    res = runner.invoke(app, ["inputs/invalidext.txt"]) 
    assert res.exit_code == 2


def test_nonexistent(runner):
    res = runner.invoke(app, ["nonexistent"]) 
    assert res.exit_code == 2
