# -*- coding: utf-8 -*-

import os
from PyInstaller.__main__ import run

if __name__ == '__main__':
    os.system('rm -rf ./dist/ASA_HMI_Data_Agent')
    os.system('pyuic5 ui/mainwindow.ui -o ui_mainwindow.py')
    os.system('pyuic5 ui/hmi.ui -o ui_hmi.py')
    os.system('pyuic5 ui/avrdude.ui -o ui_avrdude.py')
    os.system('pyuic5 ui/asa_prog.ui -o ui_asa_prog.py')
    os.system('pyuic5 ui/bit_selector.ui -o ui_bit_selector.py')
    
    opts = ['-w',
            '--paths=D:\\Compiler\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\bin',
            '--paths=D:\\Compiler\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
            '--paths=D:\\Compiler\\Python36-32\\Lib\\site-packages\\PyInstaller\\bootloader\\Windows-32bit',
            '--paths=C:\\Users\\Lite\\AppData\\Roaming\\pyinstaller\\bincache00_py36_32bit',
            '--paths=C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x86',
            '--paths=C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64',
            # '--icon', 'rxx.ico',
            '--noupx',
            '--clean',
            'main.py']

    run(opts)
    os.system('mv ./dist/main/main.exe ./dist/main/ASA_HMI_Data_Agent.exe')
    os.system('mv ./dist/main ./dist/ASA_HMI_Data_Agent')
    os.system('cp -r ./tmp ./dist/ASA_HMI_Data_Agent/tmp')
    os.system('cp ./avrdude.conf ./dist/ASA_HMI_Data_Agent/avrdude.conf')
    os.system('cp ./avrdude_settings.ini ./dist/ASA_HMI_Data_Agent/avrdude_settings.ini')
    os.system('cp ./bits_info.ini ./dist/ASA_HMI_Data_Agent/bits_info.ini')
    os.system('cp ./tools/cmd_ASA_loader.exe ./dist/ASA_HMI_Data_Agent/cmd_ASA_loader.exe')
    
    os.system('tar -zc -C ./dist -f ./dist/ASA_HMI_Data_Agent.tar.gz ./ASA_HMI_Data_Agent')
