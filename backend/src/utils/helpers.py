from typing import Dict
from urllib.parse import parse_qs


def query_string_parser(query_str: bytes) -> Dict[str, str]:
    """Parses query string in form of bytes object returned by channels into a dictionary"""
    params = parse_qs(query_str.decode("utf-8"))

    return {key: value[0] for (key, value) in params.items()}
