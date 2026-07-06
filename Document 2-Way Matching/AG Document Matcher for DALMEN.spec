# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['document_matcher_HUB.py'],
    pathex=[],
    binaries=[('C:\\Program Files\\Tesseract-OCR\\tesseract.exe', 'tesseract')],
    datas=[('C:\\Program Files\\Tesseract-OCR\\tessdata', 'tessdata'), ('C:\\poppler\\Library\\bin', 'poppler')],
    hiddenimports=['pdf2image', 'pytesseract', 'pdfplumber', 'pandas', 'openpyxl', 'PIL', 'PIL.Image'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AG Document Matcher for DALMEN',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AG Document Matcher for DALMEN',
)
