#! /usr/local/bin/python
# -*- coding: latin-1 -*-

from glob import glob
from briefcase import Briefcase

# Creating Briefcase instance.
b = Briefcase('Data.prv', '0123456789abcQW')

# Adding a few files.
ret = b.AddManyFiles(r'c:\WINDOWS\Web\Wallpaper\*.jpg', 'some pwd')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Print file list.
print
print( b.GetFileList() )
print

# Add another file.
ret = b.AddFile('readme.txt', 'pass')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Add identical file.
ret = b.AddFile('readme.txt')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Rename.
ret = b.RenFile('bliss.jpg', 'to_delete.jpg')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Properties.
print
ret = b.GetProperties('to_delete.jpg')
if ret!=-1 : print( ret )
else : print( b.lastErrorMsg )
print

# Copy.
ret = b.CopyIntoNew('to_delete.jpg', 1, 'to_execute.jpg')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Copy again, just to make sure. :)
ret = b.CopyIntoNew('to_execute.jpg', 1, 'to_delete2.jpg')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Copy error.
ret = b.CopyIntoNew('asd.jpg', 1, 'copy_error.jpg')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Delete.
ret = b.DelFile('to_delete.jpg')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Delete error.
ret = b.DelFile('to_delete.jpg')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Delete again.
ret = b.DelFile('to_delete2.jpg')
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Execute add1.
ret = b.ExportFile('readme.txt', path='d:', password='pass', execute=False)
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

# Execute addmany.
ret = b.ExportFile('to_execute.jpg', path='d:', password='some pwd', execute=False)
if not ret : print( b.lastDebugMsg )
else : print( b.lastErrorMsg )

print( 'Done !' )

# Eof()