from utils.input_manager import InputManager

def count_chars(file_path: str | None) -> int:
    with InputManager(file_path) as input:
        return sum(len(line) + 1 for line in input)
