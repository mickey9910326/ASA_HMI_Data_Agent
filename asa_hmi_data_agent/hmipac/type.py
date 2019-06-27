from struct import *
import numpy as np

def getNpType(typeNum):
    if typeNum == 0: # int8_t
        return np.int8
    elif typeNum == 1: # int16_t
        return np.int16
    elif typeNum == 2: # int32_t
        return np.int32
    elif typeNum == 3: # int64_t
        return np.int64
    elif typeNum == 4: # uint8_t
        return np.uint8
    elif typeNum == 5: # uint16_t
        return np.uint16
    elif typeNum == 6: # uint32_t
        return np.uint32
    elif typeNum == 7: # uint64_t
        return np.uint64
    elif typeNum == 8: # f32
        return np.float32
    elif typeNum == 9: # f64
        return np.float64
    else:
        return False

def getTypeStr(typeNum):
    if typeNum == 0:
        return 'i8'
    elif typeNum == 1:
        return 'i16'
    elif typeNum == 2:
        return 'i32'
    elif typeNum == 3:
        return 'i64'
    elif typeNum == 4:
        return 'ui8'
    elif typeNum == 5:
        return 'ui16'
    elif typeNum == 6:
        return 'ui32'
    elif typeNum == 7:
        return 'ui64'
    elif typeNum == 8:
        return 'f32'
    elif typeNum == 9:
        return 'f64'
    else:
        return False

def getTypeSize(typeNum):
    if typeNum == 0: # int8_t
        return 1
    elif typeNum == 1: # int16_t
        return 2
    elif typeNum == 2: # int32_t
        return 4
    elif typeNum == 3: # int64_t
        return 8
    elif typeNum == 4: # uint8_t
        return 1
    elif typeNum == 5: # uint16_t
        return 2
    elif typeNum == 6: # uint32_t
        return 4
    elif typeNum == 7: # uint64_t
        return 8
    elif typeNum == 8: # f32
        return 4
    elif typeNum == 9: # f64
        return 8
    else:
        return False

def getTypeNum(typeString):
    if typeString == 'i8': # int8_t
        return 0
    elif typeString == 'i16': # int16_t
        return 1
    elif typeString == 'i32': # int32_t
        return 2
    elif typeString == 'i64': # int64_t
        return 3
    elif typeString == 'ui8': # uint8_t
        return 4
    elif typeString == 'ui16': # uint16_t
        return 5
    elif typeString == 'ui32': # uint32_t
        return 6
    elif typeString == 'ui64': # uint64_t
        return 7
    elif typeString == 'f32': # f32
        return 8
    elif typeString == 'f64': # f64
        return 9
    elif typeString == 's': # String
        return 15
    elif typeString == 'int8': # int8_t
        return 0
    elif typeString == 'int16': # int16_t
        return 1
    elif typeString == 'int32': # int32_t
        return 2
    elif typeString == 'int64': # int64_t
        return 3
    elif typeString == 'uint8': # uint8_t
        return 4
    elif typeString == 'uint16': # uint16_t
        return 5
    elif typeString == 'uint32': # uint32_t
        return 6
    elif typeString == 'uint64': # uint64_t
        return 7
    elif typeString == 'float32': # f32
        return 8
    elif typeString == 'float64': # f64
        return 9
    elif typeString == 's': # String
        return 15
    else:
        return None

def getStTypeList(formatString):
    typeList = list()
    for typeStr in formatString.split(','):
        if typeStr=='':
            return None

        s = typeStr.split('x')
        if len(s) is not 2:
            return None
        elif s[0]=='' or s[1]=='':
            return None

        type = getTypeNum(s[0])
        if type is None:
            return None

        try:
            num = int(s[1])
        except ValueError as e:
            return None

        typeList.append({'type':type, 'num':num})
    return typeList

def getStDtype(formatString):
    args = list()
    for i, typeStr in enumerate(formatString.split(',')):
        if typeStr=='':
            return None

        s = typeStr.split('x')
        if len(s) is not 2:
            return None
        elif s[0]=='' or s[1]=='':
            return None

        type = getTypeNum(s[0])
        if type is None:
            return None

        try:
            num = int(s[1])
        except ValueError as e:
            return None

        args.append(('f'+str(i),getNpType(type),(num,)))
    dt = np.dtype(args)
    return dt


def fs2dt(formatString):
    """trans format string to numpy dtype"""
    args = list()
    for i, typeStr in enumerate(formatString.split(',')):
        if typeStr == '':
            return None

        s = typeStr.split('_')
        if len(s) is not 2:
            return None
        elif s[0] == '' or s[1] == '':
            return None

        type = getTypeNum(s[0])
        if type is None:
            return None

        try:
            num = int(s[1])
        except ValueError as e:
            return None

        args.append(('f'+str(i), getNpType(type), (num,)))
    dt = np.dtype(args)
    return dt


def getStSize(typeList):
    size = 0
    for t in typeList:
        size = size + getTypeSize(t['type']) * t['num']
    return size

def decode_struct(formatString, data):
    dt = getStDtype(formatString)
    if dt is None:
        return None
    elif dt.itemsize != len(data):
        return None
    res = np.frombuffer(data, dtype=dt, count=1)
    return np.asarray(res[0], dtype=dt)

def decode_array(typeNum, data):
    return np.frombuffer(data, dtype=getNpType(typeNum))

def npDtypeToFs(dt):
    res  = ''
    last = len(dt) - 1
    for i in range(len(dt)):
        type = getTypeStr(getTypeNum(dt[i].base.name))
        num  = dt[i].shape[0]
        res += type + '_' + str(num)
        if i != last:
            res += ','
    return res

def getFs(dt):
    return npDtypeToFs(dt)
