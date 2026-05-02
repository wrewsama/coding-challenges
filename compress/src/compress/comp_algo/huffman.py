from pathlib import Path
from typing import Optional
from heapq import heapify, heappop, heappush
import logging
import json
import struct

from compress.comp_algo.comp_algo import CompAlgo

logger = logging.getLogger(__name__)
_HEADER_LENGTH_FORMAT = ">I"

class _Node:
    _counter = 0

    def __init__(
        self,
        char: Optional[str] = None,
        left: Optional["_Node"] = None,
        right: Optional["_Node"] = None,
    ):
        self.char = char
        self.left = left
        self.right = right
        self.counter = _Node._counter
        _Node._counter += 1

    def __lt__(self, other: "_Node") -> bool:
        return self.counter < other.counter

    def __repr__(self) -> str:
        return f"_Node({self.char=}, {self.left=}, {self.right=})"

class Huffman(CompAlgo):
    def compress(self, file_path: Path, output_path: Path):
        freq_map = self._calculate_freq_map(file_path)
        if not freq_map:
            raise ValueError(f"freq map for {file_path=} is empty")

        logger.info("freqmap: %s", freq_map)
        root_node = self._generate_huffman_tree(freq_map)
        logger.info("huffman tree: %s", root_node)
        prefix_code = self._generate_prefix_code(root_node)
        logger.info("prefix codes: %s", prefix_code)
        self._write_header(output_path, prefix_code)
        self._write_compressed_data(file_path, output_path, prefix_code)

    def decompress(self, file_path: Path, output_path: Path):
        prefix_code, bytes_to_skip = self._read_header(file_path)
        logger.info("prefix code: %s, bytes to skip: %s", prefix_code, bytes_to_skip)


    def _calculate_freq_map(self, file_path: Path) -> dict[str, int]:
        freqmap = {}
        with open(file_path) as file:
            for line in file:
                for char in line:
                    freqmap[char] = freqmap.get(char, 0) + 1

        return freqmap

    def _generate_huffman_tree(self, freq_map: dict[str, int]) -> _Node:
        heap: list[tuple[int, _Node]] = []
        for char, freq in freq_map.items():
            heap.append((freq, _Node(char=char)))
        if len(heap) == 1:
            # edge case: we expect there to be at least 2 chars so the root isn't also a leaf
            # this is because we need at least 1 edge before the leaf so that we can assign a bit
            # we can just assign a dummy value since it will just get ignored
            heap.append((0, _Node(char="")))
        heapify(heap)

        while len(heap) > 1:
            freq1, node1 = heappop(heap)
            freq2, node2 = heappop(heap)
            new_node = _Node(left=node1, right=node2)
            heappush(heap, (freq1+freq2, new_node))

        return heap[0][1]

    def _generate_prefix_code(self, root_node: _Node) -> dict[str, str]:
        result: dict[str, str] = {}

        def backtrack(node: _Node, state: list[str]):
            if node.char is not None:
                result[node.char] = "".join(state)
                return

            if node.left:
                state.append("0")
                backtrack(node.left, state)
                state.pop()

            if node.right:
                state.append("1")
                backtrack(node.right, state)
                state.pop()
            
        backtrack(root_node, [])
        return result

    def _write_header(self, output_path: Path, prefix_code: dict[str, str]):
        prefix_code_bytes = json.dumps(prefix_code).encode()
        header_bytes = struct.pack(_HEADER_LENGTH_FORMAT, len(prefix_code_bytes)) + prefix_code_bytes
        output_path.write_bytes(header_bytes)

    def _write_compressed_data(self, file_path: Path, output_path: Path, prefix_code: dict[str, str]):
        with open(file_path) as infile, open(output_path, "ab") as outfile:
            buf: list[str] = []
            for line in infile:
                for bit in self._to_compressed_bitarray(line, prefix_code):
                    buf.append(bit)
                    if len(buf) == 8:
                        byte = int("".join(buf), 2).to_bytes()
                        outfile.write(byte)
                        buf = []
            remaining_bits = "".join(buf)
            if not remaining_bits:
                return

            padded = f"{remaining_bits:0<8}"
            byte = int(padded, 2).to_bytes()
            outfile.write(byte)

    def _to_compressed_bitarray(self, line: str, prefix_code: dict[str, str]) -> list[str]:
        result: list[str] = []
        for char in line:
            result.extend(prefix_code[char])
        return result
    
    def _read_header(self, file_path: Path) -> tuple[dict[str, str], int]:
        """return prefix code and total header size"""
        with open(file_path, "rb") as file:
            header_len, *_ = struct.unpack(_HEADER_LENGTH_FORMAT, file.read(4) )
            prefix_code_bytes = file.read(header_len)
        prefix_code = json.loads(prefix_code_bytes.decode())
        return prefix_code, 4+len(prefix_code_bytes)
