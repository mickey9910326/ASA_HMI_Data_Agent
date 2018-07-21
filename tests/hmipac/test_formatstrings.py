import conftest
from asa_hmi_data_agent.hmipac.type import getStTypeList

def test_t1():
    formatString = 'ui8x10'
    predict =  [{'type': 4, 'num': 10}]

    res = getStTypeList(formatString)
    assert res == predict

def test_t2():
    formatString = 'ui8x10000,f32x1'
    predict =  [{'type': 4, 'num': 10000}, {'type': 8, 'num': 1}]

    res = getStTypeList(formatString)
    assert res == predict

def test_t3():
    formatString = 'i8x1,i16x2,i32x3,i64x4,ui8x5,ui16x6,ui32x7,ui64x8,f32x9,f64x10'
    predict =  [
        {'type': 0, 'num': 1},
        {'type': 1, 'num': 2},
        {'type': 2, 'num': 3},
        {'type': 3, 'num': 4},
        {'type': 4, 'num': 5},
        {'type': 5, 'num': 6},
        {'type': 6, 'num': 7},
        {'type': 7, 'num': 8},
        {'type': 8, 'num': 9},
        {'type': 9, 'num': 10},
    ]

    res = getStTypeList(formatString)
    assert res == predict

def test_f1():
    formatString = ''
    predict = None

    res = getStTypeList(formatString)
    assert res == predict

def test_f2():
    formatString = 'ui8'
    predict = None

    res = getStTypeList(formatString)
    assert res == predict

def test_f3():
    formatString = 'ui8x'
    predict = None

    res = getStTypeList(formatString)
    assert res == predict

def test_f4():
    formatString = 'ui8x1,'
    predict = None

    res = getStTypeList(formatString)
    assert res == predict

def test_f5():
    formatString = 'ui8x1x2'
    predict = None

    res = getStTypeList(formatString)
    assert res == predict

def test_f6():
    formatString = '1x1'
    predict = None

    res = getStTypeList(formatString)
    assert res == predict

def test_f7():
    formatString = 'ui8x1.2'
    predict = None

    res = getStTypeList(formatString)
    assert res == predict

def test_f8():
    formatString = 'ui8xf1'
    predict = None

    res = getStTypeList(formatString)
    assert res == predict
