#! /usr/local/bin/python
# -*- coding: latin-1 -*-

from glob import glob
from briefcase import Briefcase

# Creating Briefcase instance.
b = Briefcase('Data.prv', '0123456789abcQW')

print( '\nAdding a few files with default pass.' )
b.AddManyFiles(r'c:\WINDOWS\Web\Wallpaper\b*.jpg', 1, 'more labels;even more labels')

print( '\nAdding a few More files with False pass.' )
b.AddManyFiles(r'c:\WINDOWS\Web\Wallpaper\t*.jpg', False)

print( '\nAdding a few More files with password.' )
b.AddManyFiles(r'c:\WINDOWS\Web\Wallpaper\a*.jpg', 'pwd', 'a;b;c;d;label')

print( '\nPrinting file list.' )
print( b.GetFileList() )

print( '\nPrinting labels list.' )
print( b.GetLabelsList() )

print( '\nAdd single file.' )
b.AddFile('GPL v3.txt', 'pass')

print( '\nRename "bliss" file.' )
b.RenFile('bliss.jpg', 'to_delete.jpg')

print( '\nCopy Bliss file, renamed as "to_delete".' )
b.CopyIntoNew('to_delete.jpg', 1, 'to_execute.jpg')

print( '\nCopy previously copied file, just to make sure.' )
b.CopyIntoNew('to_execute.jpg', 1, 'to_delete2.jpg')

print( '\nTry to copy inexistent file.' )
b.CopyIntoNew('asd.jpg', 1, 'copy_error.jpg')

print( '\nGet properties for copied/ copied/ renamed file.' )
print(b.FileStatistics('to_delete2.jpg'))

print( '\nDelete one file.' )
b.DelFile('to_delete.jpg')

print( '\nTry to delete inexistent file.' )
b.DelFile('to_delete.jpg')

print( '\nDelete another file.' )
b.DelFile('to_delete2.jpg')

print( '\nExport one file.' )
b.ExportFile('GPL v3.txt', path='d:', password='pass', execute=False)

print( '\nExport another file.' )
b.ExportFile('to_execute.jpg', path='d:', password=1, execute=False)

print( '\nExport all.' )
b.ExportAll('temp') # With default pass.
b.ExportAll('temp', False) # With false pass.
b.ExportAll('temp', 'pwd') # With password 1.
b.ExportAll('temp', 'pass') # With password 2.

print( '\nPrinting file list for the last time.' )
print( b.GetFileList() )

print( '\nDone !' )

# Eof()