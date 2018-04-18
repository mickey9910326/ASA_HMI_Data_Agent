# -*- coding: utf-8 -*-
import os
from PyInstaller.__main__ import run
import pathlib

if __name__ == '__main__':
    patch = 'v0.2.5'

    os.system('rm -rf ./dist/ASA_HMI_Data_Agent')
    os.system('pyuic5 ui/mainwindow.ui -o ui_mainwindow.py')
    os.system('pyuic5 ui/hmi.ui -o ui_hmi.py')
    os.system('pyuic5 ui/avrdude.ui -o ui_avrdude.py')
    os.system('pyuic5 ui/asa_prog.ui -o ui_asa_prog.py')
    os.system('pyuic5 ui/bit_selector.ui -o ui_bit_selector.py')

    opts = ['-w',
            # NOTE '-F' maybe not stable in some environment, need more test.
            '-F',

            # NOTE if ypu want to print debug info in CLI, use the '-debug'.
            # '--debug',

            # NOTE you need to change the libs path.
            # If it has been include in yout system PATH, you don't have to add it.
            # Need Windows Kits 10 to support win10.
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

    pathlib.Path("./dist/ASA_HMI_Data_Agent").mkdir(parents=True, exist_ok=True)
    os.system('mv ./dist/main.exe ./dist/ASA_HMI_Data_Agent/ASA_HMI_Data_Agent.exe')
    # Related files
    os.system('cp -r ./tmp ./dist/ASA_HMI_Data_Agent/tmp')
    os.system('cp -r ./tools ./dist/ASA_HMI_Data_Agent/tools')
    os.system('cp ./avrdude_settings.ini ./dist/ASA_HMI_Data_Agent/avrdude_settings.ini')
    os.system('cp ./bits_info.ini ./dist/ASA_HMI_Data_Agent/bits_info.ini')

    tarpath = './dist/' + 'ASA_HMI_Data_Agent'+ '_' + patch + '.tar.gz'
    os.system('tar -zc -C ./dist -f ' + tarpath + ' ./ASA_HMI_Data_Agent')
