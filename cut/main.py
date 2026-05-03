import argparse
from pathlib import Path

from cut import cut

def main():
    parser = argparse.ArgumentParser(description="cut from temu")
    parser.add_argument("filepath", type=Path)
    parser.add_argument("-f", "--field", type=int, required=True, help="which field to print")

    args = parser.parse_args()
    with open(args.filepath) as file:
        cut(file, args.field)

if __name__ == "__main__":
    main()
