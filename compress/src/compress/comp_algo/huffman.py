from pathlib import Path
from typing import Optional
from heapq import heapify, heappop, heappush
import logging

from compress.comp_algo.comp_algo import CompAlgo

logger = logging.getLogger(__name__)

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
        return file_path

    def decompress(self, file_path: Path, output_path: Path):
        raise NotImplementedError()

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

