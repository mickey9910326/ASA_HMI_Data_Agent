from asa_hmi_data_agent.util import ADTPATH

class AvrdudeConfParser():

    def __init__(self):
        self.confFile = ADTPATH+'/tools/avrdude.conf'

    def setConfFile(self, s):
        self.confFile = s

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
        file.close()
        return devices
