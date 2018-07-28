from .type import *
import numpy as np

__all__ = ['encodeArToPac', 'encodeStToPac']

_HEADER = b'\xab\xab\xab'

def encodeArToPac(data):
    pac  = _HEADER
    type = getTypeNum(data.dtype.name)
    data = data.tobytes()
    l    = len(data)
    pac += bytes([type, l>>8, l&0xFF])
    pac += data
    pac += bytes([sum(data)&0xFF])
    return pac

def encodeStToPac(data):
    pac  = _HEADER
    fs   = bytes(getFs(data.dtype), encoding='ascii')
    data = data.tobytes()
    l    = len(data) + len(fs) + 1
    pac += bytes([l>>8, l&0xFF, len(fs)])
    pac += fs
    pac += data
    pac += bytes([sum(data)&0xFF])
    return pac
