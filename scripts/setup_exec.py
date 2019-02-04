from scripts.util import *

import scripts.get_tool_files
import scripts.pyuic_all_ui

import scripts.build_exec.build_data_agent
import scripts.build_exec.build_adt_term
import scripts.build_exec.build_adt_loader

import os
import zipfile
import pathlib
import shutil

TARGET_ZIP = 'dist/' + 'ASA_HMI_Data_Agent'+ '_v' + VERSION + '.zip'
TARGET_DIR = 'dist/'

def rmPreFiles():
    if os.path.isdir(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)

    os.mkdir(TARGET_DIR)

def moveRelatedFiles():
    relatedFiles = ['RELEASENOTE.txt']
    relatedDirs  = []

    for file in relatedFiles:
        shutil.copyfile(file, TARGET_DIR + file)
    for dir in relatedDirs:
        shutil.copytree(dir, TARGET_DIR + dir)

def zipTargets():
    zip_dir    = TARGET_DIR
    target_zip = TARGET_ZIP

    if os.path.isfile(target_zip):
        os.remove(target_zip)

    targets = list()
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            targets += [os.path.join(root, file)]
    with zipfile.ZipFile(target_zip, 'w') as z:
        for target in targets:
            z.write(target, target.replace('dist','ASA_HMI_Data_Agent'))

def run():
    rmPreFiles()
    scripts.get_tool_files.run()
    scripts.pyuic_all_ui.run()

    scripts.build_exec.build_data_agent.run()
    scripts.build_exec.build_adt_term.run()
    scripts.build_exec.build_adt_loader.run()

    moveRelatedFiles()
    zipTargets()

if __name__ == '__main__':
    run()
