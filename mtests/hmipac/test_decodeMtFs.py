import conftest
import numpy as np
from asa_hmi_data_agent.hmipac.type import *

mfs = 'ui8_3x5'

np_type, np_shape = mtFs2Np(mfs)
print(np_type, np_shape)

res = np2MtFs(np_type, np_shape)
print(res)
