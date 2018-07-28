import numpy as np
from asa_hmi_data_agent.hmipac.type import *

def arToStr(data):
    res = ''
    t   = getTypeNum(data.dtype.name)
    data_list = data.tolist()

    res += getTypeStr(t) + ':' + '\n'
    res += align(2, data_list)
    return res

def stToStr(data):
    res = ''
    fs  = npDtypeToFs(data.dtype) # formatString
    res += fs + ': \n'
    for f in data.dtype.names:
        s = arToStr(data[f])
        s = '\n'.join('  ' + e for e in s.split('\n')[0:-1]) + '\n'
        # last item of s.split('\n') is '', so remove it
        res += s
    return res

def align(prespace, list_data):
    ls   = [str(e) for e in list_data] # list of str(data)
    maxL = max([len(s) for s in ls]) # max length of str(data)
    n    = len(list_data) # num of list_data
    res  = ''
    LINEMAX = 61 # each line string max length
    if maxL > LINEMAX:
        pass
    else:
        s = 0 # start index
        e = 0 # end index
        l = '' # each line string tmp
        q = LINEMAX // (maxL+2)
        # each data print include ',' and ' '
        e = s + q
        while e < n:
            l  = ''.join(' ' for i in range(prespace))
            l += ', '.join(('{:>'+'{:d}'.format(maxL)+'s}').format(s) for s in ls[s:e])
            l += ','
            res += l + '\n'
            s = e
            e = s + q
        l = '  ' + ', '.join(('{:>'+'{:d}'.format(maxL)+'s}').format(s) for s in ls[s:n])
        res += l + '\n'
        return res
