from compress.comp_algo.comp_algo import CompAlgo
from compress.comp_algo.huffman import Huffman


class CompAlgoFactory:
    @staticmethod
    def create(algo_name: str) -> CompAlgo:
        if algo_name == "huffman":
            return Huffman()

        raise ValueError(f"Unknown algorithm: {algo_name}")
