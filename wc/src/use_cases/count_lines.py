from utils.input_manager import InputManager

def count_lines(file_path: str | None) -> int:
    with InputManager(file_path) as input:
        return sum(1 for _ in input)
