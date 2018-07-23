#!/usr/bin/env python3
import sys
from cx_Freeze import setup,Executable
base=''
if sys.platform=='win32':
    base="Win32GUI"
packages=["idna","requests","multiprocessing"]
options={'build_exe':{'packages':packages,},}
setup(
    name='zerojudge.exe',
    version='0.1',
    options=options,
    description='zerojudge in command line',
    executables=[Executable("zerojudge-cli.py",base=base,icon="icon.ico")]
)
