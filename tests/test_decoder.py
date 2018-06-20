import conftest
import asa_hmi_data_agent.hmi.decodeASAformat as ds

text = """
ui8:
  1,2,3,4,5,6

ui16:
  5,6,7,8
 
"""

print('TestText is :')
print(text)

resArrayNums, resTypeNumList, resDataListList, res = ds.decodeTextToStruct(text)

print(res)
print(resArrayNums)
print(resTypeNumList)
print(resDataListList)
