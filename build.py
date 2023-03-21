try:
    import PyInstaller.__main__
except ImportError:
    print("PyInstaller is not installed and is required to build")
    print("To install, please run \"python -m pip -r requirements.txt\"")
    exit()

try:
    import pygame
except ImportError:
    print("Pygame is not installed and is required to build")
    print("To install, please run \"python -m pip -r requirements.txt\"")
    exit()

import os

name = ""
if os.name == "nt":
    name = "chess.exe"
elif os.name == "posix":
    name = "chess"

PyInstaller.__main__.run([
    'run.pyw',
    '--onefile',
    '--windowed',
    '-n' + name,
    "--distpath", ".",
    "--clean",
    "--log-level", "FATAL"
])

print("\n" + "="*50)
print("Compiled as \"" + name + "\" in current working directory")
print("The \"./build\" directory can be deleted safely")