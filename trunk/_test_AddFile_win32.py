#! /usr/local/bin/python
# -*- coding: latin-1 -*-

from glob import glob
from briefcase import Briefcase

# Creating Briefcase instance.
b = Briefcase('Data.prv', 'default PWD')

# Add file with password.
ret = b.AddFile('readme.txt', 'my pwd')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Add file with wrong password.
ret = b.AddFile('readme.txt', 'wrong pwd')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Add identical file with correct password.
ret = b.AddFile('readme.txt', 'my pwd')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Add identical file without password.
ret = b.AddFile('readme.txt')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Add inexisting file.
ret = b.AddFile('qwerty.txt')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Export file 1.
ret = b.ExportFile('readme.txt', password='my pwd', execute=True)
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Add file with ZERO password.
ret = b.AddFile('GPL v3.txt', False)
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Add file with ZERO password again.
ret = b.AddFile('GPL v3.txt', False)
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Export file 2.
ret = b.ExportFile('GPL v3.txt', password=False, execute=True)
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Print file list.
print
print( b.GetFileList() )
print

print( 'Done !' )

# Eof()