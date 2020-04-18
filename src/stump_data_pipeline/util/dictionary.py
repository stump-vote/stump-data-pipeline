from typing import Dict, Any

from .string import camel_to_snake


def convert_keys_from_camel_to_snake(d: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(d, dict):
        return d
    new_dict = dict()
    for k, v in d.items():
        if isinstance(v, dict):
            v = convert_keys_from_camel_to_snake(v)
        elif isinstance(v, list):
            v = [convert_keys_from_camel_to_snake(e) for e in v]
        if isinstance(k, str):
            new_dict[camel_to_snake(k)] = v
        else:
            new_dict[k] = v

    return new_dict
