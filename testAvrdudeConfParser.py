import avrdudeConfParser

praser = avrdudeConfParser.AvrdudeConfPraser()
part = praser.findPartByName(name = 'AT90CAN128')

print(part)
print(part.flashSize)
print(part.id)
print(part.desc)
print(part.signature)
print(type(part.signature))


descList = praser.listAllPartDesc()
print(descList)
