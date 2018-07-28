import conftest
import pytest
import numpy as np
from numpy.testing import assert_array_equal
from asa_hmi_data_agent.hmi.text_to_data import *

def test_getFirstArray_t1():
    text = """  // line1
    ui8:        // line2
        1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  // line3
       14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  // line4
       27, 103 // line5
               // line6   """
    predict = (
        5,
        np.array(
            [
                 1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
                14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,
                27, 103
            ],
            dtype=np.uint8
        )
    )
    res = getFirstArray(text)
    assert(res[0]==predict[0])
    assert_array_equal(res[1], predict[1])

def test_getFirstArray_t2():
    text = """  // line1
    f32:        // line2
        1e-11,   1.0,  23.0,   4.0,   5.0,   6.0,   7.0,   8.0,   2.0, // line3
        657.0,   1.0,   4.0, 324.0,  89.0  // line4      """
    predict = (
        4,
        np.array(
            [
                1e-11,   1.0,  23.0,   4.0,   5.0,   6.0,   7.0,   8.0,   2.0,
                657.0,   1.0,   4.0, 324.0,  89.0
            ],
            dtype=np.float32
        )
    )
    res = getFirstArray(text)
    assert(res[0]==predict[0])
    assert_array_equal(res[1], predict[1])

def test_getFirstArray_f1():
    text = """  // line1
    i8:        // line2
        1,2,3,4,
        """
    with pytest.raises(ValueError):
        res = getFirstArray(text)


def test_getFirstStruct_t1():
    text = """    // line1
    f32x5,i8x5:   // line2
      f32:        // line3
        1,2,3,4,5 // line4
      i8:         // line5
        1,2,3,4,5 // line6
                  // line7"""
    predict = (
        6,
        np.array(
            (
                [1,2,3,4,5],
                [1,2,3,4,5]
            ),
            dtype=
            [
                ('f0', np.float32, (5,)),
                ('f1', np.int8, (5,))
            ]
        )
    )
    res = getFirstStruct(text)
    assert(res[0] == predict[0])
    assert_array_equal(res[1], predict[1])

def test_getFirstStruct_t2():
    text = """    // line1
    f32x5:        // line2
      f32:        // line3
        1,2,3,4,5 // line4
                  """
    predict = (
        5,
        np.array(
            (
                [1,2,3,4,5],
            ),
            dtype=
            [
                ('f0', np.float32, (5,)),
            ]
        )
    )
    res = getFirstStruct(text)
    assert(res[0] == predict[0])
    assert_array_equal(res[1], predict[1])

def test_getFirstStruct_f1():
    text = """    // line1
    f32x5:        // line2
      ui8:        // line3
        1,2,3,4,5 // line4
                  """
    with pytest.raises(TypeError):
        getFirstStruct(text)

def test_getFirstStruct_f2():
    text = """    // line1
    f32x5:        // line2
      f32:        // line3
        1,2,3,4,5, // line4
                  """
    with pytest.raises(ValueError):
        res = getFirstStruct(text)

def test_textToData_t1():
    text = """    // line1
    f32x5:        // line2
      f32:        // line3
        1,2,3,4,5 // line4
                  """
    predict = [
        np.array((
                [1,2,3,4,5],
            ), dtype= [
                ('f0', np.float32, (5,)),
            ]
        )
    ]
    res = textToData(text)
    assert(res == predict)

def test_textToData_t2():
    text = """
    f32x5:
      f32:
        1,2,3,4,5
    ui8:
      1,2,3,4,5
                  """
    predict = [
        np.array((
                [1,2,3,4,5],
            ), dtype= [
                ('f0', np.float32, (5,)),
            ]
        ),
        np.array([1,2,3,4,5], dtype=np.uint8)
    ]
    res = textToData(text)
    assert_array_equal(res[0], predict[0])
    assert_array_equal(res[1], predict[1])

def test_removeSpace_t1():
    s   = '    ui8:   '
    res = removeSpace(s)
    predict = 'ui8:'
    assert(res==predict)

def test_removeComment_t1():
    s   = ' ui8: // hhh'
    res = removeComment(s)
    predict = ' ui8: '
    assert(res==predict)

def test_isCommentLine_t1():
    s = '      // comment'
    res = isCommentLine(s)
    assert(res is True)

def test_decodeTypeLine_t1():
    s   = 'ui8:'
    res = decodeTypeLine(s)
    predict = 4
    assert(res==predict)

def test_decodeTypeLine_t2():
    s   = '  i8: // comment'
    res = decodeTypeLine(s)
    predict = 0
    assert(res==predict)

def test_decodeDataLine_t1():
    s = '1,2,3,4,5,6,7,8,9'
    predict = (
        False,
        np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.int8)
    )
    res = decodeDataLine(s, 0)
    assert(res[0]==predict[0])
    assert_array_equal(res[1], predict[1])

def test_decodeDataLine_t2():
    s = '1,2,3,4,5,6,7,8,9,'
    predict = (
        True,
        np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.int8)
    )
    res = decodeDataLine(s, 0)
    assert(res[0]==predict[0])
    assert_array_equal(res[1], predict[1])
