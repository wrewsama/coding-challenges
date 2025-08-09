from rich import print, table
import typer
from typing_extensions import Annotated

from use_cases.count_bytes import count_bytes
from use_cases.count_chars import count_chars
from use_cases.count_lines import count_lines
from use_cases.count_words import count_words


def main(
    file_path: Annotated[str | None, typer.Argument()] = None,
    count_bytes_flag: Annotated[bool, typer.Option("-c")] = False,
    count_lines_flag: Annotated[bool, typer.Option("-l")] = False,
    count_words_flag: Annotated[bool, typer.Option("-w")] = False,
    count_chars_flag: Annotated[bool, typer.Option("-m")] = False,
):
    output: str | table.Table
    file_name_str = f" {file_path}" if file_path else ""
    if count_bytes_flag:
        num_bytes = count_bytes(file_path)
        output = f"\t{num_bytes}{file_name_str}"
    elif count_lines_flag:
        num_lines = count_lines(file_path)
        output = f"\t{num_lines}{file_name_str}"
    elif count_words_flag:
        num_words = count_words(file_path)
        output = f"\t{num_words}{file_name_str}"
    elif count_chars_flag:
        num_chars = count_chars(file_path)
        output = f"\t{num_chars}{file_name_str}"
    else:
        num_bytes, num_lines, num_words = count_bytes(file_path), count_lines(file_path), count_words(file_path)
        cols = ["bytes", "lines", "words"]
        data = [str(num_bytes), str(num_lines), str(num_words)]
        if file_path:
            cols.append("file")
            data.append(str(file_path))

        output_table = table.Table(*cols)
        output_table.add_row(*data)
        output = output_table

    print(output)

if __name__ == "__main__":
    typer.run(main)
