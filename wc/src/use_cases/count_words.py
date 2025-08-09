from utils.input_manager import InputManager

def count_words(file_path: str | None) -> int:
    with InputManager(file_path) as input:
        return sum(len(line.split()) for line in input)
