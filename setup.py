# -*- coding: utf-8 -*-
import os
from PyInstaller.__main__ import run
import pathlib

__VERSION__ = 'v0.4.1'

if __name__ == '__main__':

    os.system('rm -r ./dist/ASA_HMI_Data_Agent')
    os.system('pyuic5 ui/mainwindow.ui -o asa_hmi_data_agent/ui/ui_mainwindow.py')
    os.system('pyuic5 ui/hmi.ui -o asa_hmi_data_agent/ui/ui_hmi.py')
    os.system('pyuic5 ui/avrdude.ui -o asa_hmi_data_agent/ui/ui_avrdude.py')
    os.system('pyuic5 ui/asa_prog.ui -o asa_hmi_data_agent/ui/ui_asa_prog.py')
    os.system('pyuic5 ui/bit_selector.ui -o asa_hmi_data_agent/ui/ui_bit_selector.py')

    opts = [
            # NOTE '-F' maybe not stable in some environment, need more test.
            '-F',

            # NOTE if you want exe not to print info to I/O, use '-w' .
            '-w',

            # NOTE if ypu want to extra debug info, use the '-debug'.
            # '--debug',
            # '--windowed',

            # NOTE you need to change the libs path.
            # If it has been include in yout system PATH, you don't have to add it.
            # Need Windows Kits 10 to support win10.
            '--paths=D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\bin',
            '--paths=D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
            '--paths=D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyInstaller\\bootloader\\Windows-32bit',
            '--paths=C:\\Users\\Lite\\AppData\\Roaming\\pyinstaller\\bincache00_py36_32bit',
            '--paths=C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x86',
            '--paths=C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64',

            # NOTE Need DLLs in package numpy and scipy.
            '--paths=D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\scipy\\extra-dll',
            '--paths=D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\numpy\\.libs',
            # NOTE Need extra moudle in package scipy.
            '--hidden-import=scipy._lib.messagestream',

            # '--name=ASA_HMI_Data_Agent'
            # '--icon', 'rxx.ico',
            '--noupx',
            '--clean',
            'asa_hmi_data_agent/__main__.py']

    run(opts)

    pathlib.Path("./dist/ASA_HMI_Data_Agent").mkdir(parents=True, exist_ok=True)
    os.system('mv ./dist/__main__.exe ./dist/ASA_HMI_Data_Agent/ASA_HMI_Data_Agent.exe')
    # Related files
    os.system('cp -r ./tmp ./dist/ASA_HMI_Data_Agent/tmp')
    os.system('cp -r ./tools ./dist/ASA_HMI_Data_Agent/tools')
    os.system('cp -r ./settings ./dist/ASA_HMI_Data_Agent/settings')
    os.system('cp ./RELEASENOTE.txt ./dist/ASA_HMI_Data_Agent/RELEASENOTE.txt')
    tarpath = './dist/' + 'ASA_HMI_Data_Agent'+ '_' + __VERSION__ + '.tar.gz'

    os.system('tar -zc -C ./dist -f ' + tarpath + ' ./ASA_HMI_Data_Agent')
