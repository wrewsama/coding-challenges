from typing import Any, Dict

from json_parser.entities.exceptions import InvalidJsonException


def _parse_value(val: str) -> Any:
    val = val.strip()
    if not val:
        raise InvalidJsonException("empty value found")

    if val == 'null':
        return None

    if val == 'true':
        return True

    if val == 'false':
        return False

    if val[0] == '"':
        if val[-1] != '"':
            raise InvalidJsonException("quote not closed")
        return val[1:-1]

    if val.isnumeric():
        if '.' in val:
            return float(val)
        return int(val)

    raise InvalidJsonException(f"unparseable value {val}")

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
        res[k[1:-1]] = _parse_value(v)
    return res

