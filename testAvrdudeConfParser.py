import avrdudeConfParser

parser = avrdudeConfParser.AvrdudeConfParser()

s1,s2,s3 = parser.GetBasicInfoByDesc('ATmega128')

print(s1)
print(s2)
print(s3)


descList = parser.listAllPartDesc()
print(descList)
