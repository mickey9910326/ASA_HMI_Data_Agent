# NOTE you need to change the path if you want to build it.
# A path to search for imports (like using PYTHONPATH).
# If it has been include in yout system PATH, you don't have to add it.
PATH = [
    # 'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyInstaller\\bootloader\\Windows-32bit',
    # 'C:\\Users\\Lite\\AppData\\Roaming\\pyinstaller\\bincache00_py36_32bit',

    # NOTE Need libs in package PyQt5.
    'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\bin',
    'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\plugins',

    # NOTE Need Windows Kits 10 to support win10.
    'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.17763.0\\ucrt\\DLLs\\x86',
    'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\10.0.17763.0\\ucrt\\DLLs\\x64',

    # NOTE Need libs in package numpy and scipy.
    'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\scipy\\extra-dll',
    'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\numpy\\.libs',
    'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\zmq'
]

HIDEEN_IMPORT = [
    'scipy._lib.messagestream',
    'numpy.core._dtype_ctypes'
]
