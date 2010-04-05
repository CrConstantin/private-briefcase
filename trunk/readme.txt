
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
 - all files are compressed with zlib 9, and optionally crypted with AES 256;
 - you can add the same file several times, if you modify it. All changes are versioned and you can rollback anytime;
 - files can be added one by one, or multiple at the same time;
 - you can export one, or all files;
 - command line access to add, export, copy, rename and delete;
 - clean GUI to add, view, edit, version, rename and delete;
 - fast, secure, intuitive.

 - website : http://code.google.com/p/private-briefcase

------------
  Licence:
------------
  Private-Briefcase is copyright © 2010, Cristi Constantin. All rights reserved.

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
 * Python 2.6. Private-Briefcase is written entirely in Python 2.6. (www.python.org)
 * Python Crypto. Data is crypted AES 256. (www.pycrypto.org)
 * PyQt4. Graphical user interface is made with Qt. (www.riverbankcomputing.co.uk/software/pyqt/download)

---------------
  How to use:
---------------
 * In order to access Private-Briefcase classe, all you have to do is :
   "import briefcase ; b = briefcase.Briefcase()".
 * Alternatively, you can use command line to add, remove, rename or copy files from briefcase.
 * A lot of time was spent to document all modules, classes and functions in Private-Briefcase, so enjoy.
 * Note : Private-Briefcase was created on a Windows XP machine, so there might be some incompatibilities
    with other OS. Please let me know if you find any.
