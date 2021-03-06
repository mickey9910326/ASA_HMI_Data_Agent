import numpy as np
from ..hmipac.type import *
import re

# text decode
def getFirstArray(text):
    # TODO: Exception handle?
    lines = text.split('\n')
    status = int(0)
    usedLines = 0
    for i in range(len(lines)):
        s = lines[i]
        # status 0 get type
        if status == 0:
            usedLines += 1
            if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
                pass
            else:
                typeNum = decodeTypeLine(s)
                status = 1
                resdata = np.array([], getNpType(typeNum))
        # status 1 get data
        elif status == 1:
            usedLines += 1
            if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
                pass
            else:
                isContinued, data = decodeDataLine(s, typeNum)
                resdata = np.append(resdata, data)
                if isContinued is False:
                    status = 2
        # status 2 remove space lines and null line
        elif status == 2:
            if isSpaceLine(s) or isNullLine(s):
                usedLines += 1
                pass
            else:
                break
    if status == 1:
        raise ValueError()
    return usedLines, resdata


def getFirstMatrix(text):
    # TODO: Exception handle?
    lines = text.split('\n')
    status = int(0)
    usedLines = 0
    for i in range(len(lines)):
        s = lines[i]
        # status 0 get type
        if status == 0:
            usedLines += 1
            if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
                pass
            else:
                dt, shape = decodeMtFsLine(s)
                dataStr = ''
                status = 1
        # status 1 get data
        elif status == 1:
            usedLines += 1
            if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
                pass
            elif isLineLastDot(s):
                s = removeComment(s)
                s = removeSpace(s)
                dataStr += s
            else:
                s = removeComment(s)
                s = removeSpace(s)
                dataStr += s
                resdata = decodeMatrixDataText(dataStr, dt, shape)
                status = 2
        # status 2 remove space lines and null line
        elif status == 2:
            if isSpaceLine(s) or isNullLine(s):
                usedLines += 1
                pass
            else:
                break
    if status == 1:
        raise ValueError()
    return usedLines, resdata

def getFirstStruct(text):
    # TODO: Exception handle?
    lines = text.split('\n')
    usedLines = 0
    status = int(0)
    for i in range(len(lines)):
        usedLines += 1
        # get formatString
        s = lines[i]
        if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
            pass
        else:
            dt = decodeFsLine(s)
            status  = 1
            break

    # get each type data
    dataList = list()
    for idx in range(len(dt)):
        l, data = getFirstArray('\n'.join(lines[usedLines::]))
        dataList.append(data)
        usedLines += l
        if data.dtype.base.name != dt[idx].base.name:
            raise TypeError()
    resdata = np.array(tuple(dataList), dtype=dt)

    for i in range(len(lines[usedLines+1::])):
        if isSpaceLine(s) or isNullLine(s):
            usedLines += 1
        else:
            break
    return usedLines, resdata

def textToData(text):
    # TODO: Exception handle?
    res = list()
    isContinued = True
    while(isContinued):
        isContinued = False
        try:
            usedLines, data = getFirstArray(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            # print(e)
            pass
        else:
            res.append(data)
            isContinued = True
            text = '\n'.join((text.split('\n'))[usedLines::])

        try:
            usedLines, data = getFirstMatrix(text)
        except (ValueError, SyntaxError, TypeError, UnboundLocalError) as e:
            # print(e)
            pass
        else:
            res.append(data)
            isContinued = True
            text = '\n'.join((text.split('\n'))[usedLines::])

        try:
            usedLines, data = getFirstStruct(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            # print(e)
            pass
        else:
            res.append(data)
            isContinued = True
            text = '\n'.join((text.split('\n'))[usedLines::])
    return res


def isTextFormated(text):
    lines = text.split('\n')
    usedLines = 0
    status = int(0)
    i = 0
    while i < len(lines):
        s = lines[i]
        if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
            i += 1
        else:
            c = False
            try:
                usedLines, data = getFirstArray('\n'.join(lines[i::]))
            except:
                pass
            else:
                c = True

            try:
                usedLines, data = getFirstMatrix('\n'.join(lines[i::]))
            except:
                pass
            else:
                c = True
            
            try:
                usedLines, data = getFirstStruct('\n'.join(lines[i::]))
            except:
                pass
            else:
                c = True
            
            if c:
                i += usedLines
            else:
                return False
    return True


def getFirstDataType(text):
    lines = text.split('\n')
    usedLines = 0
    status = int(0)
    i = 0
    while i < len(lines):
        s = lines[i]
        if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
            i += 1
        else:
            c = False
            try:
                usedLines, data = getFirstArray('\n'.join(lines[i::]))
            except:
                pass
            else:
                return 1
                c = True

            try:
                usedLines, data = getFirstMatrix('\n'.join(lines[i::]))
            except:
                pass
            else:
                return 2

            try:
                usedLines, data = getFirstStruct('\n'.join(lines[i::]))
            except:
                pass
            else:
                return 3

            return 0


def decodeMatrixDataText(text, np_dtype, np_shape):
    """ decode data text t matrix data list
    text like [1,2,3,4,5],[6,7,8,9,10]
    """
    text = text.replace(' ', '')
    res = np.array([], dtype=np_dtype)

    a = re.findall(r'\[(.*?)\]', text)
    if len(a) != np_shape[0] :
        raise
    for b in a:
        num_str_s = b.split(',')
        if len(num_str_s) != np_shape[1]:
            raise
        d = np.array(num_str_s, dtype=np_dtype)
        res = np.append(res, d)
    
    res = res.reshape(np_shape)
    return res


def decodeText(text):
    lines = text.split('\n')
    usedLines = 0
    status = int(0)
    i = 0
    res = list()
    d = dict()
    while i < len(lines):
        s = lines[i]
        if isCommentLine(s) or isSpaceLine(s) or isNullLine(s):
            i += 1
        else:
            c = False
            try:
                usedLines, data = getFirstArray('\n'.join(lines[i::]))
            except:
                pass
            else:
                res.append(data)
                c = True

            try:
                usedLines, data = getFirstMatrix('\n'.join(lines[i::]))
            except:
                pass
            else:
                res.append(data)
                c = True

            try:
                usedLines, data = getFirstStruct('\n'.join(lines[i::]))
            except:
                pass
            else:
                res.append(data)
                c = True

            if c:
                i += usedLines
            else:
                raise 
    return res

# line decode ------------------------------------------------------------------
def decodeDataLine(s, typeNum):
    s = removeComment(s)
    s = removeSpace(s)
    isContinued = isLineLastDot(s)
    s = s[:len(s)-isContinued:].split(',')
    return isContinued, np.array(s, getNpType(typeNum))

def decodeTypeLine(s):
    s = removeComment(s)
    s = s.split(':')
    if len(s) != 2:
        return None
    return getTypeNum(removeSpace(s[0]))

def decodeFsLine(s):
    s = removeComment(s)
    s = s.split(':')
    if len(s) != 2:
        return None
    return fs2dt(removeSpace(s[0]))

def decodeMtFsLine(s):
    s = removeComment(s)
    s = s.split(':')
    if len(s) != 2:
        return None
    return mtFs2Np(removeSpace(s[0]))

# is ---------------------------------------------------------------------------
def isNullLine(s):
    return s == ''

def isSpaceLine(s):
    return s.isspace()

def isCommentLine(s):
    s = removeComment(s)
    return s.isspace() or isNullLine(s)

def isLineLastDot(s):
    if s[-1] == ',':
        return True
    return False

def isSpace(ch):
    return ch.isspace()


def isNameLine(s):
    if isCommentLine(s):
        ss = s.split('name:')
        if len(ss) != 2:
            pass
    else:
        return False
    s = removeComment(s)
    return s.isspace() or isNullLine(s)


def decodeNameLine(s):
    if isCommentLine(s):
        ss = s.split('name:')
        if len(ss) != 2:
            pass
    else:
        return False
    s = removeComment(s)
    return s.isspace() or isNullLine(s)


# remove -----------------------------------------------------------------------
def removeSpace(s):
    start = int()
    end   = int()
    for i in range(len(s)):
        if isSpace(s[i]):
            pass
        else:
            start = i
            break
    for i in range(len(s))[::-1]:
        if isSpace(s[i]):
            pass
        else:
            end = i+1
            break
    return s[start:end]

def removeComment(s):
    end = len(s)
    for i in range(len(s)):
        if s[i]=='/' and s[i+1]=='/':
            end = i
            break
    return s[:end:]
