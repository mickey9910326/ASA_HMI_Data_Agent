import conftest
from asa_hmi_data_agent.hmi.data_to_text import *
import numpy as np

# TODO changes to unit test

def test_mt2str():
    data = np.array(([1, 2, 3, 4, 5, -100, 7, 8, 9, 10, 11, 12]), np.int8).reshape(2, 6)
    mtToStr(data)

if __name__ == "__main__":
    test_mt2str()
