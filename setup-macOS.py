from cx_Freeze import setup, Executable

base = None    

executables = [Executable("zerojudge-cli.py", base=base)]

# packages = ["idna"]
options = {
    'build_exe': {    
        'packages':['bs4', 'getpass', 'lxml', 'webbrowser', 'requests', 'colorTable', 'queue', 'idna', 'sys', 'colorama'],
    },    
}

setup(
    name = "zerojudge-cli",
    options = options,
    version = "1.0",
    description = 'Build by samuel21119',
    executables = executables
)
