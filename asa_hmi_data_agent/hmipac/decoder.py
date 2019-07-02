from .type import *
from .pac_type import PacType
import enum

__all__ = ['Decoder', 'DecoderState']


def _ar_raw2ndarray(typeNum, data):
    """ transfer raw array data to ndarray type data in numpy"""
    return np.frombuffer(data, dtype=getNpType(typeNum))


def _mt_raw2ndarray(typeNum, numy, numx, data):
    """ transfer raw matrix data to ndarray type data in numpy"""
    return np.frombuffer(data, dtype=getNpType(typeNum)).reshape(numy, numx)


def _st_raw2ndarray(formatString, data):
    """ transfer raw struct data to ndarray type data in numpy"""
    dt = fs2dt(formatString)
    if dt is None:
        return None
    elif dt.itemsize != len(data):
        return None
    res = np.frombuffer(data, dtype=dt, count=1)
    return np.asarray(res[0], dtype=dt)


_CONST_HEADER = 0xac
_CONST_HEADER_NUM = 3


class InnerState(enum.IntEnum):
    STATE_HEADER_1 = 0
    STATE_HEADER_23 = 1
    STATE_LEN = 2
    STATE_CMD = 3
    STATE_CHKSUM = 4

    STATE_AR_TYPE = 11
    STATE_AR_NUM = 12
    STATE_AR_DATA_LEN = 13
    STATE_AR_DATA = 14

    STATE_MT_TYPE = 21
    STATE_MT_NUMY = 22
    STATE_MT_NUMX = 23
    STATE_MT_DATA_LEN = 24
    STATE_MT_DATA = 25

    STATE_ST_FS_LEN = 31
    STATE_ST_FS = 32
    STATE_ST_DATA_LEN = 33
    STATE_ST_DATA = 34


class DecoderState(enum.IntEnum):
    NOTPROCESSING = 0  # packet decoder doesn't start decode
    PROCESSING = 1  # packet decoder is decoding now
    DONE = 2  # packet decoding is done

globals().update(InnerState.__members__)
globals().update(PacType.__members__)
globals().update(DecoderState.__members__)


class Decoder(object):
    class StateMechine(object):
        state = int(0)
        packet_type = int(0)

        # vars for decoding array data packet
        ar_dtype = int(0)  # data type
        ar_num = int(0)  # num of data
        ar_dlen = int(0)  # data size in bytes

        # vars for decoding matrix data packet
        mt_dtype = int(0)
        mt_numy = int(0)
        mt_numx = int(0)
        mt_dlen = int(0)

        # vars for decoding struct data packet
        st_fslen = int(0)  # format string length
        st_fs = bytes()
        st_dlen = int(0)

        # vars for common use
        databuf = bytes()  # array, matrix, struct data buffer
        count = int(0)
        chksum = int(0)

    _state = DecoderState(NOTPROCESSING)
    _res = None

    def __init__(self):
        super(Decoder, self).__init__()
        self._sm = Decoder.StateMechine()

    @property
    def state(self):
        return self._state

    def get(self):
        return self._res

    def put(self, ch):
        if self._sm.state == InnerState.STATE_HEADER_1:
            if ch == _CONST_HEADER:
                self._sm.count = 1
                self._sm.state = InnerState.STATE_HEADER_23
                self._state = PROCESSING
            else:
                self._state = NOTPROCESSING

        elif self._sm.state == InnerState.STATE_HEADER_23:
            if ch == _CONST_HEADER:
                self._sm.count += 1
                if self._sm.count == 3:
                    self._sm.header = bytes(3)
                    self._sm.count = 0
                    self._sm.state = InnerState.STATE_LEN
                self._state = PROCESSING
            else:
                self._state = NOTPROCESSING

        elif self._sm.state == InnerState.STATE_LEN:
            if self._sm.count == 0:
                self._sm.pac_len = ch << 8
                self._sm.count = 1
            elif self._sm.count == 1:
                self._sm.pac_len += ch
                self._sm.count = 0
                self._sm.state = InnerState.STATE_CMD
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_CMD:
            self._sm.chksum += ch
            self._sm.packet_type = ch
            if ch == PAC_TYPE_AR:
                self._sm.state = STATE_AR_TYPE
            elif ch == PAC_TYPE_MT:
                self._sm.state = STATE_MT_TYPE
            elif ch == PAC_TYPE_ST:
                self._sm.state = STATE_ST_FS_LEN
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_AR_TYPE:
            self._sm.chksum += ch
            self._sm.ar_dtype = ch
            self._sm.state = InnerState.STATE_AR_NUM
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_AR_NUM:
            self._sm.chksum += ch
            self._sm.ar_num = ch
            self._sm.state = InnerState.STATE_AR_DATA_LEN
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_AR_DATA_LEN:
            self._sm.chksum += ch
            if self._sm.count == 0:
                self._sm.ar_dlen = ch << 8
                self._sm.count = 1
            elif self._sm.count == 1:
                self._sm.ar_dlen += ch
                self._sm.count = 0
                self._sm.databuf = bytes()
                self._sm.state = InnerState.STATE_AR_DATA
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_AR_DATA:
            self._sm.chksum += ch
            self._sm.databuf += bytes([ch])
            self._sm.count += 1
            if self._sm.count == self._sm.ar_dlen:
                self._sm.count = 0
                self._sm.state = InnerState.STATE_CHKSUM
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_MT_TYPE:
            self._sm.chksum += ch
            self._sm.mt_type = ch
            self._sm.state = InnerState.STATE_MT_NUMY
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_MT_NUMY:
            self._sm.chksum += ch
            self._sm.mt_numy = ch
            self._sm.state = InnerState.STATE_MT_NUMX
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_MT_NUMX:
            self._sm.chksum += ch
            self._sm.mt_numx = ch
            self._sm.state = InnerState.STATE_MT_DATA_LEN
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_MT_DATA_LEN:
            self._sm.chksum += ch
            if self._sm.count == 0:
                self._sm.mt_dlen = ch << 8
                self._sm.count = 1
            elif self._sm.count == 1:
                self._sm.mt_dlen += ch
                self._sm.count = 0
                self._sm.databuf = bytes()
                self._sm.state = InnerState.STATE_MT_DATA
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_MT_DATA:
            self._sm.chksum += ch
            self._sm.databuf += bytes([ch])
            self._sm.count += 1
            if self._sm.count == self._sm.mt_dlen:
                self._sm.count = 0
                self._sm.state = InnerState.STATE_CHKSUM
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_ST_FS_LEN:
            self._sm.chksum += ch
            self._sm.st_fslen = ch
            self._sm.st_fs = bytes()
            self._sm.state = InnerState.STATE_ST_FS
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_ST_FS:
            self._sm.chksum += ch
            self._sm.st_fs += bytes([ch])
            self._sm.count += 1
            if self._sm.count == self._sm.st_fslen:
                self._sm.count = 0
                self._sm.state = InnerState.STATE_ST_DATA_LEN
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_ST_DATA_LEN:
            self._sm.chksum += ch
            if self._sm.count == 0:
                self._sm.st_dlen = ch << 8
                self._sm.count = 1
            elif self._sm.count == 1:
                self._sm.st_dlen += ch
                self._sm.count = 0
                self._sm.databuf = bytes()
                self._sm.state = InnerState.STATE_ST_DATA
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_ST_DATA:
            self._sm.chksum += ch
            self._sm.databuf += bytes([ch])
            self._sm.count += 1
            if self._sm.count == self._sm.st_dlen:
                self._sm.count = 0
                self._sm.state = InnerState.STATE_CHKSUM
            self._state = PROCESSING

        elif self._sm.state == InnerState.STATE_CHKSUM:
            if self._sm.chksum & 0xFF != ch:
                self._sm.state = InnerState.STATE_HEADER_1
                self._sm.chksum = 0
                self._state = NOTPROCESSING
            else:
                self._sm.state = InnerState.STATE_HEADER_1
                self._sm.chksum = 0
                self._storeData()
                self._state = DONE

    def _storeData(self):
        self._res = dict()
        if self._sm.packet_type == PAC_TYPE_AR:
            self._res['type'] = PAC_TYPE_AR
            self._res['data'] = _ar_raw2ndarray(
                self._sm.ar_dtype,
                self._sm.databuf
            )
        elif self._sm.packet_type == PAC_TYPE_MT:
            self._res['type'] = PAC_TYPE_MT
            self._res['data'] = self._data = _mt_raw2ndarray(
                self._sm.ar_dtype,
                self._sm.mt_numy,
                self._sm.mt_numx,
                self._sm.databuf
            )
        elif self._sm.packet_type == PAC_TYPE_ST:
            self._res['type'] = PAC_TYPE_ST
            print(self._sm.st_fs)
            print(self._sm.databuf)
            self._res['data'] = _st_raw2ndarray(
                self._sm.st_fs.decode("ascii"),
                self._sm.databuf
            )
