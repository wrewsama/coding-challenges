from pathlib import Path

from compress.comp_algo.comp_algo import CompAlgo

class Huffman(CompAlgo):
    def compress(self, file_path: Path, output_path: Path):
        freqmap = {}
        with open(file_path) as file:
            for line in file:
                for char in line:
                    freqmap[char] = freqmap.get(char, 0) + 1
        print(freqmap)
        return file_path


    def decompress(self, file_path: Path, output_path: Path):
        raise NotImplementedError()
