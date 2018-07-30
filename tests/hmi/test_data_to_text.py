import conftest
from asa_hmi_data_agent.hmi.data_to_text import *
import numpy as np

# TODO changes to unit test

def test_arToStr_t1():
    data = np.array(([1, 2, 3, 4, 5]), np.int8)
    predict  = 'i8:\n'
    predict += '  1, 2, 3, 4, 5\n'
    res = arToStr(data)
    assert(res==predict)

def test_arToStr_t2():
    data = np.array(([123456789, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15]), np.int32)
    predict  = 'i32:\n'
    predict += '  123456789,         2,         3,         4,         5,\n'
    predict += '          6,         7,         8,         9,        10,\n'
    predict += '         11,        12,        13,        14,        15\n'
    res = arToStr(data)
    assert(res==predict)

def test_stToStr_t1():
    data = np.array(
        (
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5]
        ),
        dtype=[
            ('f0', np.uint8 , (5,)),
            ('f1', np.uint16, (5,))
        ]
    )

    predict  = 'ui8x5,ui16x5: \n'
    predict += '  ui8:\n'
    predict += '    1, 2, 3, 4, 5\n'
    predict += '  ui16:\n'
    predict += '    1, 2, 3, 4, 5\n'
    res = stToStr(data)
    assert(res==predict)
