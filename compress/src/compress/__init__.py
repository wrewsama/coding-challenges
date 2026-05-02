import argparse
from pathlib import Path
import logging

from compress.comp_algo.comp_algo_factory import CompAlgoFactory

logging.basicConfig(level=logging.INFO)

def main() -> None:
    parser = argparse.ArgumentParser(description="Compress files using Huffman Encoding")
    parser.add_argument("-o", "--output-path", type=Path, help="where to store the output of the compression / decompression")
    parser.add_argument("-d", "--decompress", action="store_true", help="whether to decompress the file")
    parser.add_argument("-a", "--algorithm", type=str, default="huffman", help="algorithm for compression, defaults to Huffman")
    parser.add_argument("filepath", type=Path, help="the file to compress/decompress")

    args = parser.parse_args()

    if not args.filepath.is_file():
        raise FileNotFoundError(f"File '{args.filepath}' does not exist")

    compression_algorithm = CompAlgoFactory.create(args.algorithm)

    if args.decompress:
        output_path = args.output_path or args.filepath.parent / args.filepath.stem
        compression_algorithm.decompress(args.filepath, output_path) 
        return

    output_path = args.output_path or args.filepath.parent / f"{args.filepath}.compressed"
    compression_algorithm.compress(args.filepath, output_path)

