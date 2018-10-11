import os
import glob

def run():
    uifiles = glob.glob('ui/*.ui')
    for uifile in uifiles:
        name = os.path.split(uifile)[1]
        pyfile = 'asa_hmi_data_agent\\ui\\ui_' + os.path.splitext(name)[0] + '.py'
        cmd    = 'pyuic5 ' + uifile +' -o ' + pyfile
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    run()
