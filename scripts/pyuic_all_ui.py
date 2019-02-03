import os
import glob
import platform

def run():
    uifiles = glob.glob('ui/*.ui')

    # use unix-like path style
    # it will effect line 3 in ui_xxx.py
    if platform.system() =="Windows":
        uifiles = [file.replace('\\','/') for file in uifiles]

    for uifile in uifiles:
        name = os.path.split(uifile)[1]
        pyfile = 'asa_hmi_data_agent/ui/ui_' + os.path.splitext(name)[0] + '.py'
        cmd    = 'pyuic5 ' + uifile +' -o ' + pyfile
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    run()
