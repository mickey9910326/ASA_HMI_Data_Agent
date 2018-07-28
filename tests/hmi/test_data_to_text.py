import conftest
from asa_hmi_data_agent.hmi.data_to_text import *

# TODO changes to unit test

a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,11111]
print(type(a))
res = align(2, a)
print(res)

t = np.array(a, np.uint8)
res = arToStr(t)
print(res)

t = np.array((
    [0.00000000001,1,23,4,5,6,7,8,2,657,1,4,324,89]
), np.float32)
res = arToStr(t)
print(res)

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
res = stToStr(data)
print(res)
