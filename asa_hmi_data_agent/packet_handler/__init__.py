from asa_hmi_data_agent.hmi.decodeASAformat import *

#  header of hmi get array
_CONST_HEADER_GET_AR = b'\xaa\xaa\xaa'

#  header of hmi get array
_CONST_HEADER_GET_ST = b'\xbb\xbb\xbb'


class DecoderHandler(object):
    class State(object):
        status = int(0)
        header = bytes(3)

    _text = bytes()
    _idx  = int(0)
    _state = State()
    _en_utf8 = bool(False)
    _en_big5 = bool(True)

    """docstring for Decoder."""
    def __init__(self):
        super(DecoderHandler, self).__init__()
        self._idx = int(0)

    def add_text(self, text):
        self._text += text

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def _step(self):
        if len(self._text) is 0:
            return 0, None
        for ch in self._text[self._idx::]:
            self._idx += 1
            if self._state.status is 0:
                # print('state is ' + str(self._state.status))
                if ch == b'\n' or ch == '\r':
                    pass
                    # TODO decode line
                else:
                    print(self._state.header[1:3])
                    self._state.header = self._state.header[1:3] + bytes([ch])
                if   self._state.header == _CONST_HEADER_GET_AR:
                    self._state.status = 10
                elif self._state.header == _CONST_HEADER_GET_ST:
                    self._state.status = 20
            elif self._state.status is 10:
                # print('state is ' + str(self._state.status))
                # arrTypeNum
                if ch > 9:
                    raise
                self._state.arrTypeNum = ch
                self._state.header   = bytes(3)
                self._state.status   = 11
                self._state.arrBytes = 0
                self._state.count    = 0
                self._state.chksum   = 0
            elif self._state.status is 11:
                # print('state is ' + str(self._state.status))
                self._state.arrBytes = (self._state.arrBytes<<8) + ch
                self._state.chksum  += ch
                self._state.count += 1
                if self._state.count is 2:
                    self._state.status  = 12
                    self._state.count   = 0
                    self._state.databuf = bytes()
            elif self._state.status is 12:
                # print('state is ' + str(self._state.status))
                self._state.chksum  += ch
                self._state.databuf += bytes([ch])
                self._state.count   += 1
                if self._state.count is self._state.arrBytes:
                    self._state.status  = 13
                    self.databuf = decode_array(self._state.arrTypeNum,self._state.databuf)
            elif self._state.status is 13:
                # print('state is ' + str(self._state.status))
                if self._state.chksum&0xFF is ch:
                    self._state.status = 0
                    return 1, self.databuf
                else:
                    print('arrChkSum error')
                    raise
            elif self._state.status is 20:
                pass
        return 0, None

    def get(self):
        type, data = self._step()
        if type is -1:
            # TODO handle ERROR here
            pass
        elif type is 0 :
            return None
        else:
            self.set_text(self._text[self._idx+1::])
            self._idx = 0
            return type, data

def _trans_line_to_utf8(line):
    try:
        return line.decode('utf8')
    except Exception as e:
        return None

def _trans_line_to_big5(line):
    try:
        return line.decode('big5')
    except Exception as e:
        return None

def _trans_line_to_ascii(line):
    try:
        return line.decode('ascii')
    except Exception as e:
        return None
