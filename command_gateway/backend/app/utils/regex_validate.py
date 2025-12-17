import re

def validate_regex(pattern: str):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
