from utils.input_manager import InputManager

def count_bytes(file_path: str | None) -> int:
    with InputManager(file_path, bin=True) as input:
        return sum(len(line) for line in input)

