from util import *
import conf

import scripts.get_tool_files
import scripts.pyuic_all_ui

import os
import zipfile
import pathlib
import shutil

TARGET_DIR = 'dist/'

def rmPreFiles():
    if os.path.isdir(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)

    os.mkdir(TARGET_DIR)

def run():
    rmPreFiles()
    scripts.get_tool_files.run()
    scripts.pyuic_all_ui.run()

if __name__ == '__main__':
    run()
