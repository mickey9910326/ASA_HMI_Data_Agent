# -*- coding: utf-8 -*-
import os
from PyInstaller.__main__ import run
import scripts.get_tool_files as get_tool_files
import scripts.get_tool_files as pyuic_all_ui
import zipfile
import pathlib
import shutil

__VERSION__ = 'v0.4.2'

TARGET_ZIP = 'dist/' + 'ASA_HMI_Data_Agent'+ '_' + __VERSION__ + '.zip'
TARGET_DIR = 'dist/ASA_HMI_Data_Agent'

def rmPreFiles():
    if os.path.isdir(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)

    if os.path.isfile(TARGET_ZIP):
        os.remove(TARGET_ZIP)

def renameMain():
    pathlib.Path("dist/ASA_HMI_Data_Agent").mkdir(parents=True, exist_ok=True)
    shutil.move('dist/__main__.exe', 'dist/ASA_HMI_Data_Agent/ASA_HMI_Data_Agent.exe')

def moveRelatedFiles():
    relatedFiles = ['RELEASENOTE.txt']
    relatedDirs  = ['tools', 'settings', 'tmp']

    for file in relatedFiles:
        shutil.copyfile(file, 'dist/ASA_HMI_Data_Agent/'+file)
    for dir in relatedDirs:
        shutil.copytree(dir, 'dist/ASA_HMI_Data_Agent/'+dir)

def zipTarget():
    target_zip = TARGET_ZIP
    zip_dir    = TARGET_DIR

    if os.path.isfile(target_zip):
        os.remove(target_zip)

    with zipfile.ZipFile(target_zip, 'w') as z:
        for root, dirs, files in os.walk(zip_dir):
            for file in files:
                z.write(os.path.join(root, file))

if __name__ == '__main__':
    get_tool_files.run()
    pyuic_all_ui.run()
    rmPreFiles()

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
        'asa_hmi_data_agent/__main__.py'
    ]

    run(opts)

    renameMain()
    moveRelatedFiles()
    zipTarget()
