
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "Briefcase_GUI",
        version = "1",
        description = "Briefcase Application",
        author = "Cristi Constantin",
        executables = [Executable("Briefcase_GUI.py", base = base)]
    )
