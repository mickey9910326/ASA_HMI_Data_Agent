import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executables = [
    Executable('test.py', base=base)
]

setup(name='simple_PyQt5',
      version='0.1',
      description='Sample cx_Freeze PyQt5 script',
      options=options,
      executables=executables
      )
