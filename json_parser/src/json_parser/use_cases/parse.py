from typing import Any, Dict

from json_parser.entities.exceptions import InvalidJsonException


def parse(s: str) -> Dict[str, Any]:
    if not s or s[0] != '{' or s[-1] != '}':
        raise InvalidJsonException(f"No JSON object found in {s}")

    pair_strs = s[1:-1].split(',')
    res: Dict[str, Any] = {}
    for pair_str in pair_strs:
        split = pair_str.split(":")
        if len(split) != 2:
            raise InvalidJsonException(f"Invalid KV pair {split}")
        k, v = split
        res[k[1:-1]] = v[1:-1]
    return res

