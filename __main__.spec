# -*- mode: python -*-

block_cipher = None


a = Analysis(['asa_hmi_data_agent\\__main__.py'],
             pathex=['D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\plugins', 'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyInstaller\\bootloader\\Windows-32bit', 'C:\\Users\\Lite\\AppData\\Roaming\\pyinstaller\\bincache00_py36_32bit', 'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x86', 'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64', 'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\scipy\\extra-dll', 'D:\\Programs\\Python\\Python36-32\\Lib\\site-packages\\numpy\\.libs', 'F:\\PyProjects\\ASA_HMI_Data_Agent'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='__main__',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
