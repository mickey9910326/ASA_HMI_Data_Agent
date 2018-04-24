import re
import numpy as np

class HmiDataList():

    def toString():

        pass

class line(str):
    def __new__(cls, s, row):
        obj = str.__new__(cls, s)
        obj.row = row
        return obj

    def __str__(self):
        return '\'' + self + '\', row = ' + str(self.row)

def decodeTextToArray(text):
    lines =  text.split('\n')
    res = 0
    typeNum = 0
    dataList = list()
    resText = str()

    status = 1
    for s in lines:
        if status == 1:
            if decodeIsSpaceLine(s):
                pass
            else:
                typeNum = decodeTypeLine(s)
                status = 2;
                isContinued = 1;
        elif status == 2:
            if decodeIsSpaceLine(s):
                pass
            elif (isContinued==1):
                newList, isContinued = decodeDataLine(s,typeNum)
                dataList += newList
                status = 2;
            if (isContinued==0):
                status = 3;
            if (isContinued==-1):
                res = -1
                return lineIdx, typeNum, dataList, res, resText
        elif status == 3:
            resText += s
            resText += '\n'
    return typeNum, dataList, res, resText


def _decodeHmiText(text):
    lines =  text.split('\n')
    res = 0
    typeNum = 0
    dataList = list()
    resText = str()

    status = 1
    for line in lines:
        if status is 1: # get TypeNum
            if _isSpaceStr(line):
                pass
            else:
                typeNum = _decodeTypeLine(line)
                status = 2;
                isContinued = 1;
        elif status is 2: # get Data
            if decodeIsSpaceLine(s):
                pass
            elif isContinued is 1:
                newList, isContinued = decodeDataLine(s,typeNum)
                dataList += newList
                status = 2;
            if isContinued is 0:
                status = 3;
            if isContinued is 1:
                res = -1
                return lineIdx, typeNum, dataList, res, resText
        elif status == 3:
            resText += s
            resText += '\n'
    return typeNum, dataList, res, resText

def _textToLineList(text):
    lineList = list()
    for row, str in enumerate(text.split('\n')):
        lineList.append('')


# decode Hmi Parameter Start ---------------------------------------------------
def _typeNum(s):
    """
        Decode string to typeNum.
        Return typeNum. If is not typeNum, will return -1.
    """
    # hmiTypeString section start ----------------------------------------------
    if s == 'i8': # int8_t
        return 0
    elif s == 'i16': # int16_t
        return 1
    elif s == 'i32': # int32_t
        return 2
    elif s == 'i64': # int64_t
        return 3
    elif s == 'ui8': # uint8_t
        return 4
    elif s == 'ui16': # uint16_t
        return 5
    elif s == 'ui32': # uint32_t
        return 6
    elif s == 'ui64': # uint64_t
        return 7
    elif s == 'f32': # f32
        return 8
    elif s == 'f64': # f64
        return 9
    elif s == 's': # String
        return 15
    # hmiTypeString section end ------------------------------------------------
    # stdTypeString section start ----------------------------------------------
    elif s == 'int8':
        return 0
    elif s == 'int16':
        return 1
    elif s == 'int32':
        return 2
    elif s == 'int64':
        return 3
    elif s == 'uint8':
        return 4
    elif s == 'uint16':
        return 5
    elif s == 'uint32':
        return 6
    elif s == 'uint64':
        return 7
    elif s == 'float32':
        return 8
    elif s == 'float64':
        return 9
    # stdTypeString section end ------------------------------------------------
    else:
        return -1

def _stdTypeStr(typeNum):
    if typeNum is 0:
        return 'int8'
    elif typeNum is 1:
        return 'int16'
    elif typeNum is 2:
        return 'int32'
    elif typeNum is 3:
        return 'int64'
    elif typeNum is 4:
        return 'uint8'
    elif typeNum is 5:
        return 'uint16'
    elif typeNum is 6:
        return 'uint32'
    elif typeNum is 7:
        return 'uint64'
    elif typeNum is 8:
        return 'float32'
    elif typeNum is 9:
        return 'float64'
    elif typeNum is 15: # string
        return 'int8'
    else:
        return False

def _hmiTypeStr(typeNum):
    if typeNum is 0:
        return 'i8'
    elif typeNum is 1:
        return 'i16'
    elif typeNum is 2:
        return 'i32'
    elif typeNum is 3:
        return 'i64'
    elif typeNum is 4:
        return 'ui8'
    elif typeNum is 5:
        return 'ui16'
    elif typeNum is 6:
        return 'ui32'
    elif typeNum is 7:
        return 'ui64'
    elif typeNum is 8:
        return 'f32'
    elif typeNum is 9:
        return 'f64'
    elif typeNum is 15:
        return 's'
    else:
        return False

def _packStr(typeNum):
    if typeNum == 0: # int8_t
        return 'b'
    elif typeNum == 1: # int16_t
        return 'h'
    elif typeNum == 2: # int32_t
        return 'i'
    elif typeNum == 3: # int64_t
        return 'q'
    elif typeNum == 4: # uint8_t
        return 'B'
    elif typeNum == 5: # uint16_t
        return 'H'
    elif typeNum == 6: # uint32_t
        return 'I'
    elif typeNum == 7: # uint64_t
        return 'Q'
    elif typeNum == 8: # f32
        return 'f'
    elif typeNum == 9: # f64
        return 'd'
    else:
        return False
# decode Hmi Parameter End -----------------------------------------------------

# decode String Start ----------------------------------------------------------
def _decodeTypeLine(s):
    """
        Return HmiTypeNum. If the string is wrong, will return -1.
    """
    hmiTypeStr = _removeSpace(s.split(':')[0])
    return _typeNum(hmiTypeStr)

def _isSpaceStr(s):
    if _removeSpace(s) == '':
        return True
    else:
        return False

def _isNullStr(s):
    if s == '':
        return True
    else:
        return False

def _isCommentStr(s):
    idx = s.find('\\')
    if idx is -1:
        return False
    elif _isSpaceLine(s[1:idx]):
        return True
    else:
        return False

def _removeSpace(s):
    return re.sub(' ', '', s)
# decode String End ------------------------------------------------------------
