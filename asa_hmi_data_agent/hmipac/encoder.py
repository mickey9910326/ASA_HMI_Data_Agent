from .type import *
import numpy as np
from .pac_type import PacType

__all__ = ['encodeArToPac', 'encodeStToPac', 'encodeMtToPac']


_HEADER = b'\xac\xac\xac'
globals().update(PacType.__members__)


def encodeArToPac(data):
    """
    header (3)
    pac_len (2) = 1 + 1 + 2 + N + 1 = N + 5
    pac_type (1)
    data_type (1)
    data_num (1)
    data_len (2)
    data (N)
    chknum (1) (pac_type + data_type + data_len + data)
    """

    b_pactype = bytes([PAC_TYPE_AR])

    typeNum = getTypeNum(data.dtype.name)
    b_dtype = bytes([typeNum])

    b_data = data.tobytes()
    b_datanum = bytes([len(data)])
    dlen = len(b_data)
    b_dlen = bytes([dlen >> 8, dlen & 0xFF])

    payload = b_pactype + b_dtype + b_datanum + b_dlen + b_data

    paclen = len(payload)
    b_paclen = bytes([paclen >> 8, paclen & 0xFF])

    b_chksum = bytes([sum(payload) & 0xFF])

    pac = _HEADER + b_paclen + payload + b_chksum
    
    return pac

def encodeStToPac(data):
    """
    header (3)
    pac_len (2) = 1 + 1 + M + 2 + N + 1 = N + M + 5
    pac_type (1)
    fs_len (1)
    fs (M)
    data_len (2)
    data (N)
    chknum (1) (pac_type + fs_len + fs + data_len + data)
    """

    b_pactype = bytes([PAC_TYPE_ST])

    b_fs = bytes(getFs(data.dtype), encoding='ascii')
    b_lenfs = bytes([len(b_fs)])

    b_data = data.tobytes()
    dlen = len(b_data)
    b_dlen = bytes([dlen >> 8, dlen & 0xFF])

    payload = b_pactype + b_lenfs + b_fs + b_dlen + b_data

    paclen = len(payload)
    b_paclen = bytes([paclen >> 8, paclen & 0xFF])

    b_chksum = bytes([sum(payload) & 0xFF])

    pac = _HEADER + b_paclen + payload + b_chksum

    return pac


def encodeMtToPac(data):
    """
    header (3)
    pac_len (2) = 1 + 1 + 1 + 1 + 2 + N + 1 = N + 7
    pac_type (1)
    data_type (1)
    data_dim1 (1)
    data_dim2 (1)
    data_len (2)
    data (N)
    chknum (1) (pac_type + data_type + data_len + data)
    """

    b_pactype = bytes([PAC_TYPE_MT])

    typeNum = getTypeNum(data.dtype.name)
    b_dtype = bytes([typeNum])
    b_dim1 = bytes([data.shape[0]])
    b_dim2 = bytes([data.shape[1]])

    b_data = data.tobytes()
    dlen = len(b_data)
    b_dlen = bytes([dlen >> 8, dlen & 0xFF])

    payload = b_pactype + b_dtype + b_dim1 + b_dim2 + b_dlen + b_data

    paclen = len(payload)
    b_paclen = bytes([paclen >> 8, paclen & 0xFF])

    b_chksum = bytes([sum(payload) & 0xFF])

    pac = _HEADER + b_paclen + payload + b_chksum

    return pac
