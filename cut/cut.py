from typing import IO

def cut(file: IO, field_num: int):
    for line in file:
        split = line.split()
        if len(split) < field_num:
            continue
        print(split[field_num-1]) 
