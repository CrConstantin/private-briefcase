
SET PATH="C:\Python26\Lib\site-packages\PyQt4\bin;C:\Python31\Lib\site-packages\PyQt4\bin;"+%PATH%
c:\python26\python.exe build_win32.py build_exe

copy PB.ico C:\private-briefcase /B /Y

:: Must also copy "imageformats" folder from C:\PythonXX\Lib\site-packages\PyQt4,
:: into C:\private-briefcase, or wherever you build your executable.

pause
