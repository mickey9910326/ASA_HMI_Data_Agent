from .type import *
import numpy as np

__all__ = ['encodeArToPac', 'encodeStToPac']

_HEADER = b'\xab\xab\xab'

def encodeArToPac(data):
    pac  = _HEADER
    type = getTypeNum(data.dtype.name)
    data = data.tobytes()
    l    = len(data)
    pac += bytes([type])
    length = bytes([l>>8, l&0xFF])
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
    chksum = (sum(fs+data)+len(fs))&0xFF
    pac += bytes([chksum])
    return pac
