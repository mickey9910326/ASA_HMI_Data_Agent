import conftest
from asa_hmi_data_agent.hmi.text_to_data import *

text = """
ui8_2,ui8_2:
ui8:
1,2
ui8:
1,2
"""
print(decodeFsLine('ui8_5,ui16_7'))
usedLines, resdata = getFirstStruct(text)

print(usedLines)
print(resdata)

