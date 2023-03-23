#!/usr/bin/python3
import os

print("="*os.get_terminal_size()[0] + "\n")
print("Preparing to compile to executable")
print("\n" + "="*os.get_terminal_size()[0] + "\n")

try:
    import PyInstaller.__main__
except ImportError:
    print("PyInstaller is not installed and is required to build")
    print("To install, please run \"python -m pip install -r requirements.txt --user\"")
    exit()

try:
    import pygame
except ImportError:
    print("Pygame is not installed and is required to build")
    print("To install, please run \"python -m pip install -r requirements.txt --user\"")
    exit()

print("\n" + "="*os.get_terminal_size()[0] + "\n")
print("Compilation logs\n")

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
    '-i', 'icon.ico',
    '--add-data', 'icon.ico;.',
    '--add-data', 'src/pieces/cardinal_png;src/pieces/cardinal_png',
    "--distpath", ".",
    "--clean",
    "--log-level", "FATAL"
])

print("\n" + "="*os.get_terminal_size()[0] + "\n")
print("Compiled as \"" + name + "\" in current working directory")
print("The \"./build\" directory can be deleted safely")


import sys
if sys.argv.__len__() > 1:
    if sys.argv[-1] == "--zip":
        print("\n" + "="*os.get_terminal_size()[0] + "\n")
        print("Packaging to zip file")

        import zipfile 
        from shutil import rmtree

        if ".mkzip" in os.listdir():
            rmtree(".mkzip")

        def remove_hidden(files):
            dotless = []
            for file in files:
                if file[0] == ".":
                    continue
                dotless.append(file)
            return dotless
        all_files = remove_hidden(os.listdir())
        art_files = all_files.copy()
        art_files.remove("web")

        with open(".gitignore", "r") as fp:
            gitignore = fp.read().split("\n")
            for i in gitignore:
                if i in art_files:
                    art_files.remove(i)
        
        rep_files = "web"

        os.mkdir(".mkzip")
        os.mkdir(".mkzip/Artefact")
        
        for file in art_files:
            if "." in file:
                os.symlink("../../{}".format(file), ".mkzip/Artefact/{}".format(file), target_is_directory=False)
            else:
                os.symlink("../../{}".format(file), ".mkzip/Artefact/{}".format(file), target_is_directory=True)
        
        os.symlink("../{}".format(rep_files), ".mkzip/Report", target_is_directory=True)

        def zipdir(path, ziph):
            # ziph is zipfile handle
            for root, dirs, files in os.walk(path, followlinks=True):
                for file in files:
                    ziph.write(os.path.join(root, file), 
                            os.path.relpath(os.path.join(root, file)))#, 
                                            #os.path.join(path, '..')))
        os.chdir(".mkzip/")
        with zipfile.ZipFile('../2023-219-EV-154279.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipdir('.', zipf)
        
        os.chdir("../")
        rmtree(".mkzip")

print("\n" + "="*os.get_terminal_size()[0] + "\n")
input("Completed\n... ")