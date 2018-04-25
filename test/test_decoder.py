import decodeASAformat as ds

text = str()
text += 'ui8: \n'
text += '  1,2,3,4,5,6 \n'
text += 'ui16: \n'
text += '  5,6,7,8 \n'
text = ''

print('TestText is :')
print(text)

resArrayNums, resTypeNumList, resDataListList, res = ds.decodeTextToStruct(text)

print(res)
print(resArrayNums)
print(resTypeNumList)
print(resDataListList)
