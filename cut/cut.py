from typing import IO

def cut(file: IO, field_nums: list[int], delimiter: str):
    for line in file:
        split = line.split(delimiter)
        if len(split) < max(field_nums):
            continue

        fields = [split[field_num-1] for field_num in field_nums]
        print("\t".join(fields))
