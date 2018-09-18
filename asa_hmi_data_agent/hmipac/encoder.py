from .type import *
import numpy as np

__all__ = ['encodeArToPac', 'encodeStToPac']

_HEADER = b'\xab\xab\xab'

def encodeArToPac(data):
    pac  = _HEADER
    type = getTypeNum(data.dtype.name)
    data = data.tobytes()
    l    = len(data)
    length = bytes([type, l>>8, l&0xFF])
    pac += length
    pac += data
    pac += bytes([sum(length + data)&0xFF])
    return pac

def encodeStToPac(data):
    pac  = _HEADER
    fs   = bytes(getFs(data.dtype), encoding='ascii')
    data = data.tobytes()
    l    = len(data) + len(fs)
    pac += bytes([l>>8, l&0xFF, len(fs)])
    pac += fs
    pac += data
    pac += bytes([(sum(pac) - sum(_HEADER))&0xFF])
    return pac
