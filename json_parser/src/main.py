from typing import Annotated
import os
import typer
from rich import print

from entities.exceptions import InvalidJsonException
from use_cases.parse import parse

def main(
    filepath: Annotated[str, typer.Argument()] 
):
    if not os.path.exists(filepath) or os.path.splitext(filepath) != 'json':
        raise typer.Exit(code=2)

    with open(filepath, "r") as f:
        s = "".join(line for line in f)

    try:
        res = parse(s)
    except InvalidJsonException:
        raise typer.Exit(code=1)
    else:
        print(res)

if __name__ == "__main__":
    typer.run(main)
