#! /usr/local/bin/python
# -*- coding: latin-1 -*-

from glob import glob
from briefcase import Briefcase

# Creating Briefcase instance.
b = Briefcase('DataAdd.prv', False)

print( '\nok - Add file with password.' )
b.AddFile('readme.txt', 'my pwd')

print( '\nAdd file with wrong password.' )
b.AddFile('readme.txt', 'wrong pwd')

print( '\nAdd identical file with correct password.' )
b.AddFile('readme.txt', 'my pwd')

print( '\nAdd identical file without password.' )
b.AddFile('readme.txt')

print( '\nAdd identical file with ZERO password.' )
b.AddFile('readme.txt', False)

print( '\nAdd inexisting file.' )
b.AddFile('qwerty.txt')

print( '\nok - Export file 1.' )
b.ExportFile('readme.txt', password='my pwd', execute=True)

print( '\nok - Add file with ZERO password.' )
b.AddFile('GPL v3.txt', False)

print( '\nAdd file with ZERO password again.' )
b.AddFile('GPL v3.txt', False)

print( '\nAdd file with String password again.' )
b.AddFile('GPL v3.txt', 'some password')

print( '\nok - Export file 2.' )
b.ExportFile('GPL v3.txt', password=False, execute=True)

print( '\nPrint file list.' )
print( b.GetFileList() )

print( '\nDone !' )

# Eof()