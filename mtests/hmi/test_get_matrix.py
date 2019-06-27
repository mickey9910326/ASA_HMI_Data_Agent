import conftest
from asa_hmi_data_agent.hmi.text_to_data import *

text = """
ui8_2x5:
    // name: 123
    [1,2,3,4,5],
    [6,7,8,9,10]

// 123
"""
usedLines, resdata = getFirstMatrix(text)

print(usedLines)
print(resdata)

