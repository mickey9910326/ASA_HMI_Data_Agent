from .type import *
__all__  = ['Decoder']

#  header of hmi get array
_CONST_HEADER_GET_AR = b'\xaa\xaa\xaa'

#  header of hmi get array
_CONST_HEADER_GET_ST = b'\xbb\xbb\xbb'


class Decoder(object):
    class State(object):
        status    = int(0)
        dataBytes = int(0)
        sBytes    = int(0)
        chksum    = int(0)
        count     = int(0)
        header    = bytes(3)
        databuf   = bytes()
        databuf2  = bytes()

    _text = bytes()
    _idx  = int(0)
    _state = State()
    _en_utf8 = bool(True)
    _en_big5 = bool(True)

    """docstring for Decoder."""
    def __init__(self):
        super(Decoder, self).__init__()
        self._idx = int(0)

    def add_text(self, text):
        self._text += text

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def _step(self):
        if len(self._text) == 0:
            return 0, None
        for ch in self._text[self._idx::]:
            self._idx += 1
            if self._state.status == 0:
                # print('state is ' + str(self._state.status))
                if bytes([ch]) == b'\r' or bytes([ch]) == b'\n':
                    if len(self._state.databuf) > 0:
                        res = self._decodeDatabufToStr()
                        return res
                else:
                    self._state.databuf += bytes([ch])
                    self._state.header = self._state.header[1:3] + bytes([ch])
                #
                if   self._state.header == _CONST_HEADER_GET_AR:
                    # remove 3 bytes header from databuf
                    self._state.databuf = self._state.databuf[0:-3]
                    if len(self._state.databuf) > 0:
                        res = self._decodeDatabufToStr()
                        self._resetState()
                        self._state.status = 10
                        return res
                    self._resetState()
                    self._state.status = 10
                elif self._state.header == _CONST_HEADER_GET_ST:
                    # remove 3 bytes header from databuf
                    self._state.databuf = self._state.databuf[0:-3]
                    if len(self._state.databuf) > 0:
                        res = self._decodeDatabufToStr()
                        self._resetState()
                        self._state.status = 10
                        return res
                    self._resetState()
                    self._state.status = 20
            elif self._state.status == 10:
                # print('state is ' + str(self._state.status))
                # arrTypeNum
                if ch > 9:
                    print('arrTypeNum error')
                    raise
                self._state.arrTypeNum = ch
                self._state.header   = bytes(3)
                self._state.status   = 11
                self._state.dataBytes = 0
                self._state.count    = 0
                self._state.chksum   = 0
            elif self._state.status == 11:
                # print('state is ' + str(self._state.status))
                self._state.dataBytes = (self._state.dataBytes<<8) + ch
                self._state.chksum  += ch
                self._state.count += 1
                if self._state.count == 2:
                    self._state.status  = 12
                    self._state.count   = 0
                    self._state.databuf = bytes()
            elif self._state.status == 12:
                # print('state is ' + str(self._state.status))
                self._state.chksum  += ch
                self._state.databuf += bytes([ch])
                self._state.count   += 1
                if self._state.count == self._state.dataBytes:
                    self._state.status  = 13
                    self.databuf = decode_array(self._state.arrTypeNum,self._state.databuf)
            elif self._state.status == 13:
                # print('state is ' + str(self._state.status))
                if self._state.chksum&0xFF == ch:
                    self._state.databuf = bytes()
                    self._state.status = 0
                    return 1, self.databuf
                else:
                    print('arrChkSum error')
                    self._state.databuf = bytes()
                    self._state.status = 0
                    return 1, self.databuf
                    # raise

            elif self._state.status == 20:
                # print('state is ' + str(self._state.status))
                # total bytes
                self._state.dataBytes = (self._state.dataBytes<<8) + ch
                self._state.chksum  += ch
                self._state.count   += 1
                if self._state.count == 2:
                    self._state.status  = 21
                    self._state.databuf = bytes()

            elif self._state.status == 21:
                # print('state is ' + str(self._state.status))
                # bytes of format string
                self._state.chksum  += ch
                self._state.sBytes   = ch
                self._state.status   = 22
                self._state.count    = 0
                self._state.dataBytes -= ch+1
            elif self._state.status == 22:
                # print('state is ' + str(self._state.status))
                # formatString
                self._state.chksum   += ch
                self._state.databuf2 += bytes([ch])
                self._state.count    += 1
                if self._state.count is self._state.sBytes:
                    self._state.status = 23
                    self._state.count  = 0
                    self._state.formatString = self._state.databuf2.decode("ascii")
                    self._state.databuf = bytes()

            elif self._state.status == 23:
                # print('state is ' + str(self._state.status))
                # data
                self._state.chksum  += ch
                self._state.databuf += bytes([ch])
                self._state.count   += 1
                if self._state.count == self._state.dataBytes:
                    self._state.status  = 24

            elif self._state.status == 24:
                # print('state is ' + str(self._state.status))
                # chksum
                if self._state.chksum&0xFF == ch:
                    self._state.status = 0
                    data = decode_struct( self._state.formatString, self._state.databuf )
                    self._state.databuf = bytes()
                    return 2, data
                else:
                    print('stChkSum error')
                    self._state.status = 0
                    data = decode_struct( self._state.formatString, self._state.databuf )
                    self._state.databuf = bytes()
                    return 2, data
                    # raise
        return 0, None

    def _decodeDatabufToStr(self):
        string = None
        if string is None and self._en_utf8:
            string = _trans_line_to_utf8(self._state.databuf)
        if string is None and self._en_big5:
            string = _trans_line_to_big5(self._state.databuf)
        if string is None:
            string = _trans_line_to_ascii(self._state.databuf)
        self._state.databuf = bytes()
        if string is None:
            return 0, None
        else:
            return 3, string

    def _resetState(self):
        self._state = self.State()

    def get(self):
        type, data = self._step()
        if type is -1:
            # TODO handle ERROR here
            pass
        elif type is 0 :
            return 0, None
        else:
            self.set_text(self._text[self._idx::])
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
