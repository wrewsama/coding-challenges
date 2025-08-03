from rich import print
from pathlib import Path
import typer
from typing_extensions import Annotated

from src.use_cases.count_bytes import count_bytes


def main(
    file_path: Annotated[str, typer.Argument],
    count_bytes_flag: Annotated[bool, typer.Option("-c")] = False):
    output: str
    if count_bytes_flag:
        num_bytes = count_bytes(Path(file_path))
        output = f"\t{num_bytes} {file_path}"
    else:
        raise NotImplementedError()
    print(output)

if __name__ == "__main__":
    typer.run(main)
