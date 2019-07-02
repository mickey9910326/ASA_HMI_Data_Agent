import conftest
from asa_hmi_data_agent.hmi.dec_cmd_str import *
import numpy as np

s = '~PM, Amat, ui8, 5x5'
print(decode_str(s))

s = '~PS, Cstruct, ui8_5,i16_1'
print(decode_str(s))

s = '~PA, a, ui8, 5'
print(decode_str(s))
