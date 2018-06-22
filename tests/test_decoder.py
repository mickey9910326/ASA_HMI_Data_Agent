import conftest
import asa_hmi_data_agent.hmi.decodeASAformat as ds
from asa_hmi_data_agent.hmi.decodeASAformat import getTypeNum

text_space = ""

text_single = """
ui8:
1,2,3,4,5,6
"""

text_single2 = """
ui8:
1,2,3,
4,5,6
"""

text_multi = """
ui8:
1,2,3,4,5,6
f32:
1.0 , 2, 3, 4, 5,6
i16:
1,2,3,4,5,6,7,8,9,10
"""

text_err_type = """
ui88:
1
"""

text_err_data0 = """
ui8:
1,
"""

text_err_data1 = """
ui8:
1
,
"""

text_err_data2 = """
ui8:
ss,
"""

text_err_data3 = """
ui8:
  1.2
"""

"""
return of decodeTextToStruct is
resArrayNums, resTypeNumList, resDataListList, res
"""

def test_decodeTypeLine0():
    res = ds.decodeTypeLine('  ui8:')
    assert res == getTypeNum('ui8')

def test_decodeTypeLine1():
    res = ds.decodeTypeLine('  u1:')
    assert res == -1

def test_decodeTypeLine2():
    res = ds.decodeTypeLine(' ui8')
    assert res == -1

def test_decodeTypeLine3():
    res = ds.decodeTypeLine(' ,')
    assert res == -1

def test_space_text():
    res = ds.decodeTextToStruct(text_space)
    excepted = (0,[],[],0)
    assert res == excepted

def test_single():
    res = ds.decodeTextToStruct(text_single)
    excepted = (
        1,
        [getTypeNum('ui8')],
        [[1,2,3,4,5,6]],
        0
    )
    assert res == excepted

def test_single2():
    res = ds.decodeTextToStruct(text_single)
    excepted = (
        1,
        [getTypeNum('ui8')],
        [[1,2,3,4,5,6]],
        0
    )
    assert res == excepted

def test_multi():
    res = ds.decodeTextToStruct(text_multi)
    excepted = (
        3,
        [getTypeNum('ui8'), getTypeNum('f32'), getTypeNum('i16')],
        [
            [1,2,3,4,5,6],
            [1,2,3,4,5,6],
            [1,2,3,4,5,6,7,8,9,10]
        ],
        0
    )
    assert res == excepted

def test_err_type():
    res = ds.decodeTextToStruct(text_err_type)
    excepted = (0, [], [], -1)
    assert res == excepted

def test_err_data0():
    res = ds.decodeTextToStruct(text_err_data0)
    excepted = (0, [], [], -1)
    assert res == excepted

def test_err_data1():
    res = ds.decodeTextToStruct(text_err_data1)
    excepted = (0, [], [], -1)
    assert res == excepted

def test_err_data2():
    res = ds.decodeTextToStruct(text_err_data2)
    excepted = (0, [], [], -1)
    assert res == excepted

def test_err_data3():
    res = ds.decodeTextToStruct(text_err_data3)
    excepted = (0, [], [], -1)
    assert res == excepted
