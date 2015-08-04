# -*- mode: python -*-
a = Analysis(['testClient.py'],
             pathex=['/home/cuckoo/git-TFG/test/test-exe'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='testClient',
          debug=False,
          strip=None,
          upx=True,
          console=True )
