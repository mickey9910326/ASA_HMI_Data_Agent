import conftest
import numpy as np
from asa_hmi_data_agent.hmipac.encoder import *

def test_encodeArToPac_t1():
    data = np.array(([1, 2, 3]), np.uint8)
    res = encodeArToPac(data)
    predict = b'\xab\xab\xab\x04\x00\x03\x01\x02\x03\x06'

    assert(res==predict)

def test_encodeStToPac_t1():
    data = np.array(
        (
            [1, 2],
            [1, 2]
        ),
        dtype=[
            ('f0', np.uint8 , (2,)),
            ('f1', np.uint16, (2,))
        ]
    )
    res = encodeStToPac(data)
    predict = b'\xab\xab\xab\x00\x13\x0cui8x2,ui16x2\x01\x02\x01\x00\x02\x00\x06'

    assert(res==predict)
