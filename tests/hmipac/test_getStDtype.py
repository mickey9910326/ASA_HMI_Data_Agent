import conftest
import numpy as np
from asa_hmi_data_agent.hmipac.type import getStDtype

def test_t1():
    formatString = 'ui8x10'
    predict =  np.dtype([('f0', np.uint8, (10,))])

    res = getStDtype(formatString)
    assert res == predict

def test_t2():
    formatString = 'ui8x10000,f32x1'
    predict = np.dtype([
        ('f0', np.uint8  , (10000,)),
        ('f1', np.float32, (1,)    ),
    ])

    res = getStDtype(formatString)
    assert res == predict

def test_t3():
    formatString = 'i8x1,i16x2,i32x3,i64x4,ui8x5,ui16x6,ui32x7,ui64x8,f32x9,f64x10'
    predict = np.dtype([
        ('f0', np.int8   , (1,)),
        ('f1', np.int16  , (2,)),
        ('f2', np.int32  , (3,)),
        ('f3', np.int64  , (4,)),
        ('f4', np.uint8  , (5,)),
        ('f5', np.uint16 , (6,)),
        ('f6', np.uint32 , (7,)),
        ('f7', np.uint64 , (8,)),
        ('f8', np.float32, (9,)),
        ('f9', np.float64, (10,)),
    ])

    res = getStDtype(formatString)
    assert res == predict

def test_f1():
    formatString = ''
    predict = None

    res = getStDtype(formatString)
    assert res == predict

def test_f2():
    formatString = 'ui8'
    predict = None

    res = getStDtype(formatString)
    assert res == predict

def test_f3():
    formatString = 'ui8x'
    predict = None

    res = getStDtype(formatString)
    assert res == predict

def test_f4():
    formatString = 'ui8x1,'
    predict = None

    res = getStDtype(formatString)
    assert res == predict

def test_f5():
    formatString = 'ui8x1x2'
    predict = None

    res = getStDtype(formatString)
    assert res == predict

def test_f6():
    formatString = '1x1'
    predict = None

    res = getStDtype(formatString)
    assert res == predict

def test_f7():
    formatString = 'ui8x1.2'
    predict = None

    res = getStDtype(formatString)
    assert res == predict

def test_f8():
    formatString = 'ui8xf1'
    predict = None

    res = getStDtype(formatString)
    assert res == predict
