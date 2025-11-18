# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['image_downloader.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ImageDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Fenster-App ohne Terminal
)

app = BUNDLE(
    exe,
    name='ImageDownloader.app',
    icon=None,             # später z.B. 'icon.icns'
    bundle_identifier=None # optional eigene Bundle-ID
)
