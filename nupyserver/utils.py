import codecs
import hashlib
from os.path import exists, isfile
from typing import IO


def hash_file(file, method=hashlib.sha256(), bufsize=65536):
    try:
        f = file if type(file) is IO else open(file, 'rb')
        while True:
            data = f.read(bufsize)
            if not data:
                break
            method.update(data)
    except IOError as err:
        raise err
    finally:
        if not type(file) is IO and f:
            f.close()

    return method


def detect_codec(data, default='utf-8'):
    """
    Detect file encoding
    Copyright by ivan_pozdeev
    https://stackoverflow.com/a/24370596
    :param data: bytearray or path to file
    :param default: default codec to use
    :return: the detected codec
    """

    raw = None
    if type(data) is str and exists(data) and isfile(data):
        with open(data, 'rb') as f:
            raw = f.read(4)
    elif type(data) is bytes:
        raw = data[0:4]
    else:
        raise IOError('only file path or binary data allowed')

    # BOM_UTF32_LE's start is equal to BOM_UTF16_LE so need to try the former first
    for enc, boms in \
            ('utf-8-sig', (codecs.BOM_UTF8,)), \
            ('utf-16', (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)), \
            ('utf-32', (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        if any(raw.startswith(bom) for bom in boms):
            return enc

    return default


def get_localip() -> str:
    """
    Get local ip address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception as _:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_value(key: str, d: dict, default=None):
    """
    Search dictionary for key case insensitive and returns value
    :param key: key in dictionary
    :param d: dictionary
    :param default:
    :return: None if not found otherwise default
    """

    for k in d:
        if k.lower() == key.lower():
            return d[k]

    return default
