import conf
import os
import urllib.request
from zipfile import ZipFile

TARGETDIR = 'asa_hmi_data_agent/tools'

def run():
    if os.path.isdir(TARGETDIR) is False:
        os.mkdir(TARGETDIR)

    getAvrduee()
    getM128STK500()

def getAvrduee():
    url  = 'http://download.savannah.gnu.org/releases/avrdude/avrdude-6.3-mingw32.zip'
    file = 'avrdude-6.3-mingw32.zip'

    if os.path.isfile(file) is False:
        urllib.request.urlretrieve(url, file)
        try:
            res = urllib.request.urlretrieve(url, file)
        except:
            print('Unable to get file from ' + url)
            raise

        with ZipFile(file, 'r') as z:
            z.extractall(path=TARGETDIR)

def getM128STK500():
    url  = 'https://github.com/nuclear-refugee/bootloader/releases/download/0.1.1/m128_stk500.hex'
    file = TARGETDIR + '/m128_stk500.hex'

    if os.path.isfile(file) is False:
        try:
            res = urllib.request.urlretrieve(url, file)
        except:
            print('Unable to get file from ' + url)
            raise

if __name__ == '__main__':
    run()
