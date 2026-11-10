import codecs
from pathlib import Path

string_types = str,


def bytes_to_int(val):
    return int(codecs.encode(val, 'hex'), 16)


def pick_name(filename, candidates):
    filedir = Path(filename).parent
    name_lower = Path(filename).name.lower()
    name_candidate = None

    for name in candidates:

        if name_lower == Path(name).name.lower():
            name_candidate = str(filedir / name)
            break

    if name_candidate:
        filename = name_candidate

    return filename
