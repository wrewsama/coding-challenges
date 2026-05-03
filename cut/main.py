import argparse
from pathlib import Path
import sys

from cut import cut

_STDIN_FILEPATH = Path("-")

def _parse_fields(raw_fields: str) -> list[int]:
    field_delimiter = "," if "," in raw_fields else " "
    return [int(field) for field in raw_fields.split(field_delimiter)]

def main():
    parser = argparse.ArgumentParser(description="cut from temu")
    parser.add_argument("filepath", type=Path, nargs="?")
    parser.add_argument("-f", "--fields", type=_parse_fields, required=True)
    parser.add_argument("-d", "--delimiter", default="\t")

    args = parser.parse_args()
    if not args.filepath or args.filepath == _STDIN_FILEPATH:
        cut(sys.stdin, args.fields, args.delimiter)
        return

    with open(args.filepath) as file:
        cut(file, args.fields, args.delimiter)

if __name__ == "__main__":
    main()
