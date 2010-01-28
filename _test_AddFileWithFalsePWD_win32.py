#! /usr/local/bin/python
# -*- coding: latin-1 -*-

from glob import glob
from briefcase import Briefcase

# Creating Briefcase instance.
b = Briefcase('DataAdd.prv', False)

print( '\npass - Add file with password.' )
b.AddFile('readme.txt', 'my pwd')

print( '\nfail - Add file with wrong password.' )
b.AddFile('readme.txt', 'wrong pwd')

print( '\nfail - Add identical file with correct password.' )
b.AddFile('readme.txt', 'my pwd')

print( '\nfail - Add identical file without password.' )
b.AddFile('readme.txt')

print( '\nfail - Add identical file with ZERO password.' )
b.AddFile('readme.txt', False)

print( '\nfail - Add inexisting file.' )
b.AddFile('qwerty.txt')

print( '\npass - Export file 1.' )
b.ExportFile('readme.txt', password='my pwd', execute=True)

print( '\npass - Add file with ZERO password.' )
b.AddFile('GPL v3.txt', False)

print( '\nfail - Add file with ZERO password again.' )
b.AddFile('GPL v3.txt', False)

print( '\nfail - Add file with String password again.' )
b.AddFile('GPL v3.txt', 'some password')

print( '\npass - Export file 2.' )
b.ExportFile('GPL v3.txt', password=False, execute=True)

print( '\nPrint file list.' )
print( b.GetFileList() )

print( '\nDone !' )

# Eof()