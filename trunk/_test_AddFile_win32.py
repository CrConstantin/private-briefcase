#! /usr/local/bin/python
# -*- coding: latin-1 -*-

from glob import glob
from briefcase import Briefcase

# Creating Briefcase instance.
b = Briefcase('Data.prv', 'default PWD')

print( '\nAdd file with password.' )
b.AddFile('readme.txt', 'my pwd')

print( '\nAdd file with wrong password.' )
b.AddFile('readme.txt', 'wrong pwd')

print( '\nAdd identical file with correct password.' )
b.AddFile('readme.txt', 'my pwd')

print( '\nAdd identical file without password.' )
b.AddFile('readme.txt')

print( '\nAdd inexisting file.' )
b.AddFile('qwerty.txt')

print( '\nExport file 1.' )
b.ExportFile('readme.txt', password='my pwd', execute=True)

print( '\nAdd file with ZERO password.' )
b.AddFile('GPL v3.txt', False)

print( '\nAdd file with ZERO password again.' )
b.AddFile('GPL v3.txt', False)

print( '\nExport file 2.' )
b.ExportFile('GPL v3.txt', password=False, execute=True)

print( '\nPrint file list.' )
print( b.GetFileList() )

print( '\nDone !' )

# Eof()