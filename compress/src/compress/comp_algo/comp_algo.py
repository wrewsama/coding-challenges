from abc import ABC, abstractmethod
from pathlib import Path

class CompAlgo(ABC):
    @abstractmethod
    def compress(self, file_path: Path, output_path: Path) -> Path:
        ...

    @abstractmethod
    def decompress(self, file_path: Path, output_path: Path) -> Path:
        ... 
