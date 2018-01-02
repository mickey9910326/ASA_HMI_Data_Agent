from struct import *

def decode_array(typeNum,data):
    if typeNum == 0:
        # int8_t
        typeS = 'b'
        typeByte = 1
    elif typeNum == 1:
        # int16_t
        typeS = 'h'
        typeByte = 2
    elif typeNum == 2:
        # int32_t
        typeS = 'i'
        typeByte = 4
    elif typeNum == 3:
        # int64_t
        typeS = 'q'
        typeByte = 8
    elif typeNum == 4:
        # uint8_t
        typeS = 'B'
        typeByte = 1
    elif typeNum == 5:
        # uint16_t
        typeS = 'H'
        typeByte = 2
    elif typeNum == 6:
        # uint32_t
        typeS = 'I'
        typeByte = 4
    elif typeNum == 7:
        # uint64_t
        typeS = 'Q'
        typeByte = 8
    elif typeNum == 8:
        # f32
        typeS = 'f'
        typeByte = 4
    elif typeNum == 9:
        # f64
        typeS = 'd'
        typeByte = 8
    else:
        return False
    return unpack('<'+str(int(round(len(data)/typeByte)))+typeS, data)

def decodePackStr(typeNum):
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
    elif typeNum == 15:
        return 's'
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
    elif typeNum == 15: # String
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
    else:
        return -1

def decodeTextToArrey(text):
    # decode Data Type
    lines =  text.split('\n')
    res = 0
    typeNum = 0
    dataList = list()
    resText = str();

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

def decodeTextToStruct(text):
    # decode Data Type
    lines =  text.split('\n')
    res = 0
    lineIdx = 0
    dataList = list()

    resTypeNumList = list()
    resDataListList = list()
    resArrayNums = 0

    status = 1
    for s in lines:
        if status == 1:
            if decodeIsSpaceLine(s):
                pass
            else:
                typeNum = decodeTypeLine(s)
                status = 2;
                isContinued = 1;
                dataList = list();
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
                return lineIdx, typeNum, dataList, res
        if status == 3:
            # res data
            resTypeNumList.append(typeNum)
            resDataListList.append(dataList)
            resArrayNums +=1
            status = 1;
    # while res!=-1 and lineIdx != len(lines):
    #     # decode Type
    #     typeLine = lines[lineIdx]
    #     typeNum = decodeTypeLine(typeLine)
    #     if typeNum == -1:
    #         res = -1
    #         return lineIdx, typeNum, dataList, res
    #     # decode Data
    #     lineIdx += 1
    #     isContinued = 1
    #     while isContinued == 1:
    #         newList, isContinued = decodeDataLine(lines[lineIdx],typeNum)
    #         dataList += newList
    #         lineIdx += 1
    #     if isContinued == -1:
    #         res = -1;\

    return resArrayNums, resTypeNumList, resDataListList, res

def isNum(ch):
    if ch > '0' and ch < '9': # space
        return True
    return False

def isLowerAlphabet(ch):
    if ch > 'a' and ch < 'z': # space
        return True
    return False

def decodeIsSpaceLine(s):
    for ch in s:
        if ch == '\x20': # space
            pass
        else:
            return False
    return True

def decodeTypeLine(s):
    resTypeString = str();
    typeNum = -1
    status = 0
    for ch in s:
        if status == 0: # remove space
            if ch == '\x20': # space
                pass
            elif isNum(ch) or isLowerAlphabet(ch):
                status = 1
            else:
                status = 99
        if status == 1:
            if isNum(ch) or isLowerAlphabet(ch):
                resTypeString += str(ch);
            else:
                status = 2
        if status == 2:
            if ch == '\x20': # space
                pass
            elif ch == ':':
                status = 3
            else:
                print('sys : type line error : ' + s)
                return -1
        if status == 3:
            resTypeNum = getTypeNum(resTypeString)
            print('sys : get type num of \'' + resTypeString + '\' is ' + str(resTypeNum))
            return resTypeNum
            break
    return -1

def decodeDataLine(s,typeNum):
    # typeLineArr = list(lines.pop(0)).reverse();
    print('sys : decode Data Line : ' + s)
    datas = s.split(',')
    resDataList = list();
    if typeNum>=0 and typeNum<=7:
        isInt = 1
    elif typeNum>=8 and typeNum<=9:
        isInt = 0
    else:
        return 0,-1
    for data in datas:
        try:
            if isInt:
                num = int(data)
            else:
                num = float(data)
            resDataList.append(num)
        except (ValueError,SyntaxError):
            for ch in data:
                if ch == '\x20': # space
                    pass
                else:
                    return resDataList, -1
            return resDataList, 1
    return resDataList, 0

def decodeFormatString(s):
    typeStrs = s.split(',')
    typeNumList = list();
    typeDataNumList = list();
    for typeStr in typeStrs:
        deTypeStr = typeStr.split('x')
        print(deTypeStr)
        typeNumList.append(getTypeNum(deTypeStr[0]))
        typeDataNumList.append(int(deTypeStr[1]))
    return typeNumList,typeDataNumList

def decode_struct(totalBytes,formatString,data):
    dataBytes = totalBytes-len(formatString)-1;
    typeNumList , typeDataNumList = decodeFormatString(formatString)
    dataIdx = 0;
    dataLastIdx = 0;
    dataListList = list();
    for idx in range(len(typeNumList)):
        dataLastIdx = dataIdx + getTypeSize(typeNumList[idx])*typeDataNumList[idx]
        dataList = unpack('<'+str(typeDataNumList[idx])+decodePackStr(typeNumList[idx]), data[dataIdx:dataLastIdx])
        dataIdx = dataLastIdx
        dataListList.append(dataList)
    return typeNumList, dataListList

def transUi8ToString(text):
    # decode Data Type
    lines =  text.split('\n')
    res = 0
    lineIdx = 0
    dataList = list()
    resText = str()

    resTypeNumList = list()
    resDataListList = list()
    resArrayNums = 0

    status = 1
    for idx,s in enumerate(lines):
        if status == 1:
            if decodeIsSpaceLine(s):
                resText += s
                if idx+1 == len(lines):
                    pass
                else:
                    resText += '\n'
                pass
            else:
                typeNum = decodeTypeLine(s)
                if typeNum == 4:
                    resText += 's:'
                    resText += '\n'
                    status = 2;
                    isContinued = 1;
                else:
                    resText += s
                    resText += '\n'
        elif status == 2:
            if decodeIsSpaceLine(s):
                resText += s
                resText += '\n'
                pass
            elif (isContinued==1):
                newList, isContinued = decodeDataLine(s,typeNum)
                dataList += newList
                status = 2;
            if (isContinued==0):
                # status = 3;
                status = 1;
                resText += '  \''
                resText += bytes(dataList).decode("utf-8")
                resText += '\'\n'
                dataList = list()
            if (isContinued==-1):
                res = -1
                return res, resText
    return res, resText

def transStringToUi8(text):
    # decode Data Type
    lines =  text.split('\n')
    res = 0
    lineIdx = 0
    dataList = list()
    resText = str()

    resTypeNumList = list()
    resDataListList = list()
    resArrayNums = 0

    status = 1
    for idx,s in enumerate(lines):
        if status == 1:
            if decodeIsSpaceLine(s):
                resText += s
                if idx+1 == len(lines):
                    pass
                else:
                    resText += '\n'
                pass
            else:
                typeNum = decodeTypeLine(s)
                if typeNum == 15:
                    resText += 'ui8:'
                    resText += '\n'
                    status = 2;
                    isContinued = 1;
                else:
                    resText += s
                    resText += '\n'
        elif status == 2:
            start = s.find('\'')
            end   = s.rfind('\'')
            status = 3
            print(start)
            print(end)
            datas = s[start+1:end]
            print(datas)
            print(datas.encode())
            datas = s[start+1:end].encode()

            s = '  '
            for idx, data in enumerate(datas):
                s += str((data))
                if idx+1 != len(datas):
                    s += ',  '
                else:
                    resText += s
                    resText += '\n'
                    s = '  '
                if len(s) > 100: #換行
                    resText += s
                    resText += '\n'
                    s = '  '
            status = 1
    return res, resText
