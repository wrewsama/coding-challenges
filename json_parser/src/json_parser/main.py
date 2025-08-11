from typing import Annotated
import os
import typer
from rich import print

from json_parser.entities.exceptions import InvalidJsonException
from json_parser.use_cases.parse import parse

app = typer.Typer()

@app.command()
def main(
    raw_filepath: Annotated[str, typer.Argument()] 
):
    filepath = os.path.expandvars(raw_filepath)
    if not os.path.exists(filepath) or os.path.splitext(filepath)[1] != '.json':
        raise typer.Exit(code=2)

    with open(filepath, "r") as f:
        s = "".join(line for line in f).strip()

    try:
        res = parse(s)
    except InvalidJsonException as e:
        print(f"ERROR: {e}")
        raise typer.Exit(code=1)
    else:
        print(res)


if __name__ == "__main__":
    typer.run(main)
