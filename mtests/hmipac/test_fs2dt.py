import conftest
import numpy as np
from asa_hmi_data_agent.hmipac.type import *

fs = 'ui8_5,ui16_7'

dt = fs2dt(fs)

print(dt)
