from pathlib import Path

def count_bytes(file_path: Path) -> int:
    return file_path.stat().st_size

