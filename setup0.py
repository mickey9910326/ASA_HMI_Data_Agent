# -*- coding: utf-8 -*-
"""
Tis script will force compress libs into one file.
And it is not stable now.
"""
import os
from PyInstaller.__main__ import run
import pathlib

if __name__ == '__main__':
    os.system('rm -rf ./dist/ASA_HMI_Data_Agent2')
    os.system('pyuic5 ui/mainwindow.ui -o ui_mainwindow.py')
    os.system('pyuic5 ui/hmi.ui -o ui_hmi.py')
    os.system('pyuic5 ui/avrdude.ui -o ui_avrdude.py')
    os.system('pyuic5 ui/asa_prog.ui -o ui_asa_prog.py')
    os.system('pyuic5 ui/bit_selector.ui -o ui_bit_selector.py')
    
    opts = ['-w',
            '-F',
            # '--debug',
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

    pathlib.Path("./dist/ASA_HMI_Data_Agent2").mkdir(parents=True, exist_ok=True)
    os.system('mv ./dist/main.exe ./dist/ASA_HMI_Data_Agent2/ASA_HMI_Data_Agent.exe')
    # Related files
    os.system('cp -r ./tmp ./dist/ASA_HMI_Data_Agent2/tmp')
    os.system('cp -r ./tools ./dist/ASA_HMI_Data_Agent2/tools')
    os.system('cp ./avrdude_settings.ini ./dist/ASA_HMI_Data_Agent2/avrdude_settings.ini')
    os.system('cp ./bits_info.ini ./dist/ASA_HMI_Data_Agent2/bits_info.ini')
    
    os.system('tar -zc -C ./dist -f ./dist/ASA_HMI_Data_Agent2.tar.gz ./ASA_HMI_Data_Agent2')
