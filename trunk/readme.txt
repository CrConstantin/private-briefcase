
 * Private-Briefcase Project Documentation *

-------------
  Contents:
-------------

 - About
 - Licence
 - Requirements
 - How to use

###############

----------
  About:
----------

 - keeps all your private files in one place, on HDD, in one big database;
 - each file has its own metadata like: description, tags, etc;
 - files are compressed with zlib 6 or bz2 9 and optionally encrypted with AES 256,
   using the global database password, or a separate password;
 - you can add the same file several times. All changes are versioned and you can rollback anytime;
 - files can be added one by one, or multiple at the same time;
 - you can export one, or all files;
 - command line access to add, export, copy, rename and delete;
 - clean GUI to add, view, edit, export, version, rename and delete;
 - fast, secure, intuitive;

 - website : http://private-briefcase.googlecode.com

------------
  Licence:
------------
  Private-Briefcase is copyright © 2010-2012, Cristi Constantin. All rights reserved.

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  If you redistribute this software, neither the name of "Private-Briefcase"
  nor the names of its contributors may be used to endorse or promote
  products derived from this software without specific prior written
  permission.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License (GPL) for more details.

  You have received a copy of the GNU General Public License along
  with this program.

-----------------
  Requirements:
-----------------
 * Python 2.6 or 2.7. Private-Briefcase is written entirely in Python 2. (www.python.org)
 * Python Crypto. Data is encrypted with AES 256. (www.pycrypto.org)
 * PyQt4. Graphical user interface with Qt. (www.riverbankcomputing.co.uk/software/pyqt/download)

---------------
  How to use:
---------------
 * Graphical user interface can be accesed by opening "briefcase_GUI.py".
 * Alternatively, you can use command line to add, remove, rename or copy files into/ from briefcase files.
 * In order to access Private-Briefcase class, all you have to do is : "import briefcase".
 * A lot of time was spent to document all modules, classes and functions in Private-Briefcase, so enjoy.
 * Note : Private-Briefcase was tested on Windows XP/ Windows 7/ Ubuntu, so there might be a few
    incompatibilities with other OS-es. Please let me know if you find any.
