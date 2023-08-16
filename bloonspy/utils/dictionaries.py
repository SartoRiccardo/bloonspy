from typing import Dict, Any, List, Tuple


def rename_keys(dictionary: Dict[str, Any], keys: List[Tuple[str, str]]) -> Dict[str, Any]:
    new_dict = {}
    for old_key, new_key in keys:
        item = dictionary
        current_keys = old_key.split(".")
        while len(current_keys) > 0:
            key = current_keys.pop(0)
            if key not in item:
                item = None
                break
            item = item[key]
        if item is not None:
            new_dict[new_key] = item

    return new_dict


def has_all_keys(dictionary: Dict[str, Any], key_list: List[str]):
    for key in key_list:
        if key not in dictionary.keys():
            return False
    return True


def enum_any_dict(enum_cls, raw_dict, parse_raw: callable = lambda x: x) -> dict:
    result = {}
    for key in raw_dict.keys():
        result[enum_cls.from_string(key)] = parse_raw(raw_dict[key])
    return result
