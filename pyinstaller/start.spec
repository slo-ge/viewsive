# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['..\\src\\start.py'],
             pathex=['C:\\Users\\Philipp\\PycharmProjects\\cef-multiwindow'],
             binaries=[],
             datas=[(HOMEPATH + '\\PyQt5\\Qt\\bin\*', 'PyQt5\\Qt\\bin')],
             hiddenimports=['json', 'PyQt5','PyQt5.QtNetwork','PyQt5.QtMultimedia','PyQt5.QtCore','PyQt5.QtGui','PyQt5.QtWidgets'],
             hookspath=["."],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=True,
             win_private_assemblies=True,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(
        a.pure,
        a.zipped_data,
        cipher=block_cipher
)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='start',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='start')
