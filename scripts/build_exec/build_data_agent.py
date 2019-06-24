import PyInstaller.__main__
import scripts.build_exec.util as util
import conf

import shutil

def rename_exec():
    shutil.move('dist/__main__.exe', 'dist/ASA_HMI_Data_Agent.exe')

def getRelatedFiles():
    relatedDirs  = ['tools', 'settings', 'tmp']

    for dir in relatedDirs:
        shutil.copytree('asa_hmi_data_agent/'+dir, 'dist/'+dir)

def build_exec():
    opts  = ['asa_hmi_data_agent/__main__.py']
    opts += ['--noupx', '--clean']

    # NOTE '--onefile' Create a one-file bundled executable.
    # maybe not stable in some environment, need more test.
    opts += ['--onefile']

    # NOTE if you want exe not to print info to I/O, use '-w' .
    opts += ['-w']

    # NOTE if ypu want to extra debug info, use the '-debug'.
    # opts += ['--debug']

    opts += ['--path={}'.format(path) for path in util.PATH]
    opts += ['--hidden-import={}'.format(path) for path in util.HIDEEN_IMPORT]
    # print(opts)
    PyInstaller.__main__.run(opts)

def run():
    build_exec()
    rename_exec()
    getRelatedFiles()

if __name__ == '__main__':
    run()
