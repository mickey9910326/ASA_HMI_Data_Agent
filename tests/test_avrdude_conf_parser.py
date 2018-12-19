import conftest
from asa_hmi_data_agent.avrdude.avrdudeConfParser import AvrdudeConfParser

if __name__ == '__main__':
    parser = AvrdudeConfParser()

    s1,s2,s3 = parser.GetBasicInfoByDesc('ATmega128')

    print(s1)
    print(s2)
    print(s3)

    descList = parser.listAllPartDesc()
    print(len(descList))
    print(descList)

    devices = parser.GetDeviceInfo()

    print(len(devices))
    for device in devices:
        print(device)
