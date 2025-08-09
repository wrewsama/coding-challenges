import sys
from typing import IO


class InputManager:
    def __init__(self, file_path: str | None, bin: bool = False):
        self.is_file = file_path is not None
        self.io: IO 
        if not file_path:
            self.io = sys.stdin
            return
        mode = "rb" if bin else "r"
        self.io = open(file_path, mode)
    
    def __enter__(self):
        return self.io

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_file:
            self.io.close()
