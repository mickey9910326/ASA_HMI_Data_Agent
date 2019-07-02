import re

__all__ = ['decode_cmd']

def decode_cmd(s):
    # TODO 用正規表達 取代以下判斷式
    res = dict()
    if s[0] == b'~'[0]:
        if s[1:3] == b'PA':
            res['cmd'] = 'put'
            res['class'] = 'array'
            ss = s.split(b',')
            res['fs'] = ss[1].replace(b' ', b'')
            return res

        elif s[1:3] == b'PM':
            res['cmd']   = 'put'
            res['class'] = 'matrix'
            ss = s.split(b',')
            res['fs'] = ss[1].replace(b' ', b'')
            return res

        elif s[1:3] == b'PS':
            res['cmd']   = 'put'
            res['class'] = 'struct'
            res['fs'] = b','.join(s.split(b',')[1::]).replace(b' ', b'')
            return res

        elif s[1:3] == b'GA':
            res['cmd'] = 'get'
            res['class'] = 'array'
            ss = s.split(b',')
            res['fs'] = ss[1].replace(b' ', b'')
            return res

        elif s[1:3] == b'GM':
            res['cmd'] = 'get'
            res['class'] = 'matrix'
            ss = s.split(b',')
            res['fs'] = ss[1].replace(b' ', b'')
            return res

        elif s[1:3] == b'GS':
            res['cmd'] = 'get'
            res['class'] = 'struct'
            res['fs'] = b''.join(s.split(b',')[1::]).replace(b' ', b'')
            return res

        elif s[1:4] == b'ACK':
            res['cmd'] = 'ack'
            return res

    else:
        return None


def decode_cmd_with_name(s):
    # TODO 用正規表達 取代以下判斷式
    res = dict()
    if s[0] == '~':
        if s[1:3] == 'PA':
            res['cmd'] = 'put'
            res['class'] = 'array'
            ss = s.split(',')
            res['name'] = ss[1].replace(' ', '')
            res['type'] = ss[2].replace(' ', '')
            res['num'] = int(ss[3])
            return res

        elif s[1:3] == 'PM':
            res['cmd']   = 'put'
            res['class'] = 'matrix'
            ss = s.split(',')
            res['name'] = ss[1].replace(' ', '')
            res['type'] = ss[2].replace(' ', '')
            s_numy, s_numx = ss[3].split('x')
            res['numx'] = int(s_numx)
            res['numy'] = int(s_numy)
            return res

        elif s[1:3] == 'PS':
            res['cmd']   = 'put'
            res['class'] = 'struct'
            ss = s.split(',')
            res['name'] = ss[1].replace(' ', '')
            res['fs'] = ','.join(ss[2::]).replace(' ', '')
            return res

        elif s[1:3] == 'GA':
            res['cmd'] = 'get'
            res['class'] = 'array'
            ss = s.split(',')
            res['name'] = ss[1].replace(' ', '')
            res['type'] = ss[2].replace(' ', '')
            res['num'] = int(ss[3])
            return res

        elif s[1:3] == 'GM':
            res['cmd'] = 'get'
            res['class'] = 'matrix'
            ss = s.split(',')
            res['name'] = ss[1].replace(' ', '')
            res['type'] = ss[2].replace(' ', '')
            s_numy, s_numx = ss[3].split('x')
            res['numx'] = int(s_numx)
            res['numy'] = int(s_numy)
            return res

        elif s[1:3] == 'GS':
            res['cmd'] = 'get'
            res['class'] = 'struct'
            ss = s.split(',')
            res['name'] = ss[1].replace(' ', '')
            res['fs'] = ','.join(ss[2::]).replace(' ', '')
            return res

        elif s[1:4] == 'ACK':
            res['cmd'] = 'ack'

    else:
        return None
