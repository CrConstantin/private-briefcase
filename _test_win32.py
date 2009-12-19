#! /usr/local/bin/python
# -*- coding: latin-1 -*-

from glob import glob
from briefcase import Briefcase

# Creating Briefcase instance.
b = Briefcase('Data.prv', '0123456789abcQWE')

# Adding a few files.
b.AddManyFiles(r'c:\WINDOWS\Web\Wallpaper\*.jpg')

# Add more files.
b.AddFile('readme.txt')
b.AddFile('readme.txt')

# Rename.
b.RenFile('bliss.jpg', 'to_delete.jpg')

# Copy.
b.CopyIntoNew('to_delete.jpg', 1, 'to_execute.jpg')
# Copy again, just to make sure. :)
b.CopyIntoNew('to_execute.jpg', 1, 'to_delete2.jpg')

# Delete.
b.DelFile('to_delete.jpg')
b.DelFile('to_delete2.jpg')

# Execute.
b.ExportFile('to_execute.jpg', path='d:', execute=False)
#b.ExportFile('readme.txt', execute=True)

print( 'Done !' )

# Eof()