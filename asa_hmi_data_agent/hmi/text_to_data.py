import numpy as np
from ..hmipac.type import *

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
            usedLines, data = getFirstStruct(text)
        except (ValueError,SyntaxError,TypeError,UnboundLocalError) as e:
            # print(e)
            pass
        else:
            res.append(data)
            isContinued = True
            text = '\n'.join((text.split('\n'))[usedLines::])
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
    return getStDtype(removeSpace(s[0]))

# is ---------------------------------------------------------------------------
def isNullLine(s):
    return s == ''

def isSpaceLine(s):
    return s.isspace()

def isCommentLine(s):
    return removeComment(s).isspace()

def isLineLastDot(s):
    if s[-1] == ',':
        return True
    return False

def isSpace(ch):
    return ch.isspace()

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
