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
                if line.find('desc') is 4:
                    descList.append(line.split('\"')[1])
                    status = 1
        return descList
    #---- listAllPartDesc End --------------------------------------------------

    #---- GetBasicInfoByDesc Start ---------------------------------------------
    def GetBasicInfoByDesc(self, desc):
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
                if line.find('desc') is 4:
                    descList.append(line.split('\"')[1])
                    status = 1

            if status is 1:
                if line.find('part') is 0:
                    status = 2
            elif status is 2: # id
                if line.find('id') is 4:
                    status = 3
                    id =  line.split('\"')[1]
            elif status is 3: # desc
                if line.find('desc') is 4:
                    if line.split('\"')[1].find(desc) is 0:
                        desc = line.split('\"')[1]
                        status = 4
                    else :
                        status = 1

            elif status is 4: # signature
                if line.find('signature') is 4:
                    signature = line[line.find('=')+2:line.find(';')].split(' ')
                    return desc, id, signature
        return None, None, None
    #---- GetBasicInfoByDesc End -----------------------------------------------

    #---- findPartByName Start -------------------------------------------------
    # def findPartByDesc(self, desc):
    #     file = open(self.confFile,"r")
    #     lineidx = 0
    #     i = 0
    #     status = 1
    #     part = Part()
    #     print(name)
    #     while 1:
    #         lineidx = lineidx+1
    #         line = file.readline()
    #         if line is '':
    #             break
    #
    #         if status is 1:
    #             if line.find('part') is 0:
    #                 status = 2
    #         elif status is 2: # id
    #             if line.find('id') is 4:
    #                 status = 3
    #                 part.id = line.split('\"')[1]
    #         elif status is 3: # desc
    #             if line.find('desc') is 4:
    #                 if line.split('\"')[1].find(desc) is 0:
    #                     part.desc = line.split('\"')[1]
    #                     status = 4
    #                 else :
    #                     status = 1
    #         elif status is 4: # signature
    #             if line.find('signature') is 4:
    #                 part.signature = line[line.find('=')+2:line.find(';')].split(' ')
    #                 status = 5
    #
    #         elif status is 5: # eeprom size
    #             if line.find('memory \"eeprom\"') is 4:
    #                 status = 6
    #         elif status is 6:
    #             if line.find('size') is 8:
    #                 part.eepromSize = int(line[line.find('=')+1:line.find(';')])
    #                 status = 7
    #
    #         elif status is 7: # flash size
    #             if line.find('memory \"flash\"') is 4:
    #                 status = 8
    #         elif status is 8:
    #             if line.find('size') is 8:
    #                 part.flashSize = int(line[line.find('=')+1:line.find(';')])
    #                 status = 9
    #         elif status is 9:
    #             return part
    #     return None
    #---- findPartByName End ---------------------------------------------------

    #---- findPartByid Start ---------------------------------------------------
    # def findPartById(self, id):
    #     file = open(self.confFile,"r")
    #     lineidx = 0
    #     i = 0
    #     status = 1
    #     part = Part()
    #     while 1:
    #         lineidx = lineidx+1
    #         line = file.readline()
    #         if line is '':
    #             break
    #
    #         if status is 1:
    #             if   line.find('part parent') is 0:
    #                 part.hasParent = True
    #                 part.parentId = line.split('\"')[1]
    #                 status = 2
    #             elif line.find('part') is 0:
    #                 status = 2
    #         elif status is 2: # id
    #             if line.find('id') is 4:
    #                 if line.split('\"')[1].find(id) is 0:
    #                     part.id = line.split('\"')[1]
    #                     status = 3
    #                 else :
    #                     status = 1
    #             else:
    #                 part.hasParent = False
    #         elif status is 3: # desc
    #             if line.find('desc') is 4:
    #                 part.desc = line.split('\"')[1]
    #                 status = 4
    #         elif status is 4: # signature
    #             if line.find('signature') is 4:
    #                 part.signature = line[line.find('=')+2:line.find(';')].split(' ')
    #                 if part.hasParent:
    #                     status = 10
    #                 else:
    #                     status = 5
    #
    #         elif status is 5: # eeprom size
    #             if line.find('memory \"eeprom\"') is 4:
    #                 status = 6
    #         elif status is 6:
    #             if line.find('size') is 8:
    #                 part.eepromSize = int(line[line.find('=')+1:line.find(';')])
    #                 status = 7
    #
    #         elif status is 7: # flash size
    #             if line.find('memory \"flash\"') is 4:
    #                 status = 8
    #         elif status is 8:
    #             if line.find('size') is 8:
    #                 part.flashSize = int(line[line.find('=')+1:line.find(';')])
    #                 status = 9
    #
    #         elif status is 9:
    #             return part
    #
    #         elif status is 10:
    #             print (part.parentId)
    #             partParent = self.findPartById(part.parentId)
    #             part.eepromSize = partParent.eepromSize
    #             part.flashSize  = partParent.flashSize
    #             return part
    #
    #     return None
    #---- findPartByid End -----------------------------------------------------
