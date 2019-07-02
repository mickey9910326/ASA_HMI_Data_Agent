import conftest
from asa_hmi_data_agent.hmicmd.decode import *
import numpy as np

s = b'~PM, ui8_5x5'
print(decode_cmd(s))

s = b'~PS, ui8_5,i16_1'
print(decode_cmd(s))

s = b'~PA, ui8_5'
print(decode_cmd(s))
