import conftest
import numpy as np
from asa_hmi_data_agent.hmipac.type import npDtypeToFs

def test_t1():
    dt =  np.dtype([('f0', np.uint8, (10,))])
    predict = 'ui8x10'

    res = npDtypeToFs(dt)
    assert res == predict

def test_t2():
    dt = np.dtype([
        ('f0', np.uint8  , (10000,)),
        ('f1', np.float32, (1,)    ),
    ])
    predict = 'ui8x10000,f32x1'

    res = npDtypeToFs(dt)
    assert res == predict

def test_t3():
    dt = np.dtype([
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
    predict = 'i8x1,i16x2,i32x3,i64x4,ui8x5,ui16x6,ui32x7,ui64x8,f32x9,f64x10'

    res = npDtypeToFs(dt)
    assert res == predict
