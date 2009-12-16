
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

 - keeps your private files in one place, on HDD, in one big database;
 - all files are compressed with zlib 9, and crypted with AES 256;
 - you can add the same file several times. All changes are versioned and you can rollback anytime;
 - you can add one, or multiple files;
 - you can export one, or multiple files;
 - command line access to add and export, copy rename and delete;
 - fast, secure, intuitive.

------------
  Licence:
------------
  Private-Briefcase is copyright © 2009, Cristi Constantin. All rights reserved.

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

---------------
  How to use:
---------------
 * In order to access Private-Briefcase classe, all you have to do is :
   "import briefcase ; b = briefcase.Briefcase()".
 * Alternatively, you can use command line to add, remove, rename or copy files from briefcase.
 * A LOT of time was spent to document all modules, classes and functions in Private-Briefcase, so enjoy.
 * Note : Letter-Monster was created on a Windows XP machine, so there might be some incompatibilities with other OS.
    Please let me know if you find any.
