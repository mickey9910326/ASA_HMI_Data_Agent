# class Part:
#     id   = str()
#     desc = str()
#     signature  = []
#     flashSize  = int()
#     eepromSize = int()
#     def __init__(self):
#         pass

class AvrdudeConfParser():
    """docstring for AvrdudeConfParser."""

    def __init__(self):
        self.confFile = 'tools/avrdude.conf'

    def setConfFile(self, s):
        self.confFile = s

    #---- listAllPartDesc Start ------------------------------------------------
    def listAllPartDesc(self):
        descList = list()
        file = open(self.confFile,"r")
        status = 1
        while 1:
            line = file.readline()
            if line is '':
                break
            elif line[0] is '#':
                continue

            if status is 1:
                if line.find('part') is 0:
                    status = 2
            elif status is 2: # desc
                idx = line.find('desc')
                if idx is 4 or idx is 5:
                    descList.append(line.split('\"')[1])
                    status = 1
        return descList
    #---- listAllPartDesc End --------------------------------------------------

    #---- GetBasicInfoByDesc Start ---------------------------------------------
    def GetBasicInfoByDesc(self, desc):
        file = open(self.confFile,"r")
        status = 1
        while 1:
            line = file.readline()
            if line is '':
                break
            elif line[0] is '#':
                continue

            if status is 1:
                if line.find('part') is 0:
                    status = 2
            elif status is 2: # id
                idx = line.find('id')
                if idx is 4 or idx is 5:
                    status = 3
                    id =  line.split('\"')[1]
            elif status is 3: # desc
                idx = line.find('desc')
                if idx is 4 or idx is 5:
                    if line.split('\"')[1].find(desc) is 0:
                        desc = line.split('\"')[1]
                        status = 4
                    else :
                        status = 1

            elif status is 4: # signature
                idx = line.find('signature')
                if idx is 4 or idx is 5:
                    signature = line[line.find('=')+2:line.find(';')].split(' ')
                    return desc, id, signature
        return None, None, None
    #---- GetBasicInfoByDesc End -----------------------------------------------

    #---- GetDeviceInfo Start ---------------------------------------------
    def GetDeviceInfo(self):
        file = open(self.confFile,"r")
        status = 1
        devices = list()
        while 1:
            line = file.readline()
            if line is '':
                break
            elif line[0] is '#':
                continue

            if status is 1:
                if line.find('part') is 0:
                    status = 2
            elif status is 2: # id
                idx = line.find('id')
                if idx is 4 or idx is 5:
                    id =  line.split('\"')[1]
                    status = 3
            elif status is 3: # desc
                idx = line.find('desc')
                if idx is 4 or idx is 5:
                    desc = line.split('\"')[1]
                    if len(desc) > 18:
                        status = 1
                        # remove desc like 'AVR XMEGA family common values'
                    else:
                        status = 4
            elif status is 4: # signature
                idx = line.find('signature')
                if idx is 4 or idx is 5:
                    signature = line[line.find('=')+2:line.find(';')].split(' ')
                    devices.append({
                        'desc' : desc,
                        'id' : id,
                        'signature' : signature
                    })
                    status = 1
        return devices
    #---- GetDeviceInfo End -----------------------------------------------
