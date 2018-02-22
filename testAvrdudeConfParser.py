import avrdudeConfParser

praser = avrdudeConfParser.AvrdudeConfPraser()

s1,s2,s3 = praser.GetBasicInfoByDesc('ATmega128')

print(s1)
print(s2)
print(s3)


descList = praser.listAllPartDesc()
print(descList)
