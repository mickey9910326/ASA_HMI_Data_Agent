import conftest
from asa_hmi_data_agent.hmi.hmi_load_dialog import reStructureData
import numpy as np

def test_reStructureData_t1():
    data = np.array(
        [[(
            np.array([[1.11]], dtype=np.float32),
            np.array([[ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10]], dtype=np.uint8)
        )]],
        dtype=[('f0', 'O'), ('f1', 'O')]
    )
    predict = np.array(
        (
            [1.11],
            [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10]
        ),
        dtype=[('f0', '<f4', (1,)), ('f1', 'u1', (10,))]
    )

    res = reStructureData(data)
    assert(res==predict)
