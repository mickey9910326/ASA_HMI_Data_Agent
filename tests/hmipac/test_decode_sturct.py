import conftest
from asa_hmi_data_agent.hmipac.type import decode_struct
import numpy as np
from numpy.testing import assert_array_equal

def test_t1():
    formatString = 'ui8x5'
    data = b'\x01\x02\x03\x04\x05'
    predict = np.array(
        (
            [1, 2, 3, 4, 5],
        ),
        dtype=[
            ('f0', np.uint8, (5,))
        ]
    )

    res = decode_struct(formatString, data)
    assert_array_equal(res, predict)

def test_t2():
    formatString = 'ui8x5,ui16x5'
    data  = b'\x01\x02\x03\x04\x05'
    data += b'\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00'
    predict = np.array(
        (
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5]
        ),
        dtype=[
            ('f0', np.uint8 , (5,)),
            ('f1', np.uint16, (5,))
        ]
    )

    res = decode_struct(formatString, data)
    assert_array_equal(res, predict)

def test_t3():
    formatString = 'ui8x1,ui16x2'
    formatString = 'i8x1,i16x2,i32x3,i64x4,ui8x5,ui16x6,ui32x7,ui64x8'
    data  = np.array([ 1], dtype=np.int8).tobytes()
    data += np.array([ 2, 3], dtype=np.int16).tobytes()
    data += np.array([ 4, 5, 6], dtype=np.int32).tobytes()
    data += np.array([ 7, 8, 9,10], dtype=np.int64).tobytes()
    data += np.array([10,11,12,13,14], dtype=np.uint8).tobytes()
    data += np.array([15,16,17,18,19,20], dtype=np.uint16).tobytes()
    data += np.array([21,22,23,24,25,26,27], dtype=np.uint32).tobytes()
    data += np.array([28,29,30,31,32,33,34,35], dtype=np.uint64).tobytes()
    predict = np.array(
        (
            [ 1],
            [ 2, 3],
            [ 4, 5, 6],
            [ 7, 8, 9,10],
            [10,11,12,13,14],
            [15,16,17,18,19,20],
            [21,22,23,24,25,26,27],
            [28,29,30,31,32,33,34,35],
        ),
        dtype=[
            ('f0', np.int8  , (1,)),
            ('f1', np.int16 , (2,)),
            ('f2', np.int32 , (3,)),
            ('f3', np.int64 , (4,)),
            ('f4', np.uint8 , (5,)),
            ('f5', np.uint16, (6,)),
            ('f6', np.uint32, (7,)),
            ('f7', np.uint64, (8,))
        ]
    )

    res = decode_struct(formatString, data)
    assert_array_equal(res, predict)

def test_t4():
    formatString = 'f32x5,f64x5'
    data  = np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype=np.float32).tobytes()
    data += np.array([1.2, 2.3, 3.4, 4.5, 5.6], dtype=np.float64).tobytes()
    predict = np.array(
        (
            [1.1, 2.2, 3.3, 4.4, 5.5],
            [1.2, 2.3, 3.4, 4.5, 5.6]
        ),
        dtype=[
            ('f0', np.float32, (5,)),
            ('f1', np.float64, (5,))
        ]
    )

    res = decode_struct(formatString, data)
    assert_array_equal(res, predict)

def test_f1():
    formatString = 'f32x10'
    data  = np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype=np.float32).tobytes()
    predict = None

    res = decode_struct(formatString, data)
    assert_array_equal(res, predict)
