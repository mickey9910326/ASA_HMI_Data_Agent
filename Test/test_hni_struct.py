from hmi.decodeASAformat import *

if __name__ == "__main__":
    typeNumList , typeDataNumList = decodeFormatString('ui8x4,f32x5')
    print(typeNumList)
    print(typeDataNumList)

    formatString = 'ui8x5,i16'
    totalBytes
    decode_struct(totalBytes,formatString,data)
