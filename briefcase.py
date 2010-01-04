# -*- coding: latin-1 -*-

'''
    Briefcase-Project v1.0 \n\
    Copyright © 2009-2010, Cristi Constantin. All rights reserved. \n\
    This module contains Briefcase class with all its functions. \n\
    Tested on Windows XP, with Python 2.6. \n\
    External dependencies : Python Crypto. \n\
'''

# Standard libraries.
import os, sys
import shutil
import glob
import sqlite3
import zlib
import tempfile
import hashlib
from time import clock
from time import strftime

# External dependency.
from Crypto.Cipher import AES
from Crypto.Hash import MD4

__version__ = '1.0'
__all__ = ['Briefcase']


class Briefcase:
    """ Main class """

    def __init__(self, database='Data.prv', password=''):
        '''
        Create new Database, or connect to an old Database. \n\
        If you don't know the correct password, you cannot acces the crypted data from tables,
        so don't delete the code that checks the password. Make sure you remember the password. \n\
        One SQLITE3 file for each Briefcase instance. \n\
        '''
        #
        self.database = str(database)
        self.lastErrorMsg = ''
        self.lastDebugMsg = ''
        #
        if os.path.exists(self.database):
            exists_db = True
        else:
            exists_db = False

        self.conn = sqlite3.connect(self.database)
        self.c = self.conn.cursor()
        md5 = hashlib.md5(password)

        if exists_db:
            self.pwd = self.c.execute('select pwd from prv').fetchone()[0]
            if self.pwd != md5.hexdigest():
                raise Exception('The password is INCORRECT! You will not be able to decrypt any data!')
        else:
            self.pwd = md5.hexdigest()
            # Prv table contains the password and the original names of the files.
            self.c.execute('create table prv (pwd TEXT unique, file TEXT)')
            self.c.execute('insert into prv (pwd) values (?)', [self.pwd])
            self.conn.commit()
        #


    def _transformb(self, bdata):
        '''
        Transforms any binary data into ready-to-write SQL information. \n\
        '''
        crypt = AES.new(self.pwd)
        vCompressed = zlib.compress(bdata,9)
        L = len(vCompressed)
        vCrypt = crypt.encrypt(vCompressed + 'X' * ((((L/16)+1)*16)-L))
        return buffer(vCrypt)


    def _restoreb(self, bdata):
        '''
        Restores binary data from SQL information. \n\
        '''
        crypt = AES.new(self.pwd)
        vCompressed = crypt.decrypt(bdata)
        return zlib.decompress(vCompressed)


    def AddFile(self, filepath, versionable=True):
        '''
        If file doesn't exist in database, create the file. If file exists, add another row. \n\
        Table name is MD4 Hexdigest of the file name (lower case). \n\
        Each row contains : Version, Raw-data, Hash of original data. \n\
        Raw-data is : original binary data -> crypted -> compressed. \n\
        Versionable=False checks if the file is in the database. If it is, an error is raised
        and the file is not added. \n\
        '''
        ti = clock()
        fpath = filepath.lower()
        md4 = MD4.new( os.path.split(fpath)[1] )
        filename = 't'+md4.hexdigest()
        del md4

        if not os.path.exists(filepath):
            self.lastErrorMsg = 'Func AddFile: file path "%s" doesn\'t exist!' % filepath
            return -1

        # Try to create the table.
        try:
            self.c.execute('create table %s (version integer primary key asc, raw BLOB, hash TEXT,'
                'date TEXT, user TEXT)' % filename)
        # If the table is already created and versionable is false, raise error and exit. Else, pass.
        except:
            if not versionable:
                self.lastErrorMsg = 'Func AddFile: you selected versionable=False, so no new version '\
                    'will be added!'
                return -1

        # Read and transform all binary data.
        f = open(filepath, 'rb').read()
        raw = self._transformb(f)
        md4 = MD4.new(f)
        hash = md4.hexdigest()
        del f, md4

        # Check if the new file is identical with the latest version.
        old_hash = self.c.execute('select hash from %s order by version desc' % filename).fetchone()
        if old_hash and hash == old_hash[0]:
            self.lastErrorMsg = 'Func AddFile: file "%s" is IDENTICAL with the version stored in the '\
                'database!' % os.path.split(fpath)[1]
            return -1

        self.c.execute(('insert into %s (raw, hash, date, user) values (?,?,?,?)' % filename), [raw, hash,
            strftime("%Y-%b-%d %H:%M:%S"), os.getenv('USERNAME')])
        self.c.execute('insert or abort into prv (file) values (?)', [os.path.split(fpath)[1]])
        self.conn.commit()

        ver_max = self.c.execute('select version from %s order by version desc' % filename).fetchone()
        self.lastDebugMsg = 'Adding file "%s" version "%i" took %.4f sec.' % (filepath, ver_max[0], clock()-ti)
        return 0


    def AddManyFiles(self, pathregex, versionable=True):
        '''
        Add more files, using a pattern. \n\
        If file doesn't exist in database, create the file. If file exists, add another row. \n\
        Versionable=False checks if the file is in the database. If it is, an error is raised
        and the file is not added. \n\
        '''
        ti = clock()
        path = os.path.split(pathregex)[0]
        pathreg = pathregex.replace('[', '[[]') # Fix possible bug in Windows ?

        if not os.path.exists(path):
            self.lastErrorMsg = 'Func AddManyFiles: path "%s" doesn\'t exist!' % path
            return -1

        files = glob.glob(pathreg)

        if not len(files):
            self.lastErrorMsg = 'Func AddManyFiles: there are no files to match "%s"!' % pathregex
            return -1
        for file in files:
            self.AddFile(file, versionable)

        self.lastDebugMsg = 'Added %i files in %.4f sec.' % (len(files), clock()-ti)
        return 0


    def CopyIntoNew(self, fname, version, new_fname):
        '''
        Copy one version of one file, into a new file, that will have version 1. \n\
        '''
        ti = clock()
        if ('\\' in new_fname) or ('/' in new_fname) or (':' in new_fname) or ('*' in new_fname) \
            or ('?' in new_fname) or ('"' in new_fname) or ('<' in new_fname) or ('>' in new_fname) \
            or ('|' in new_fname):
            self.lastErrorMsg = 'Func CopyIntoNew: a filename cannot contain any of the following '\
                'characters  \\ / : * ? " < > |'
            return -1

        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4
        md4 = MD4.new( new_fname.lower() )
        new_filename = 't'+md4.hexdigest()
        del md4

        if self.c.execute('select * from prv where file="%s"' % (new_fname.lower())).fetchone():
            self.lastErrorMsg = 'Func CopyIntoNew: there is already a file called "%s"!' % new_fname
            return -1

        try:
            data = self.c.execute('select raw, hash from %s where version=%i' % (filename, version)).fetchone()
            self.c.execute('create table %s (version integer primary key asc, raw BLOB, hash TEXT,'
                'date TEXT, user TEXT)' % new_filename)
            self.c.execute(('insert into %s (raw, hash, date, user) values (?,?,?,?)' % new_filename),
                [data[0], data[1], strftime("%Y-%b-%d %H:%M:%S"), os.getenv('USERNAME')])
            self.c.execute('insert into prv (file) values (?)', [new_fname.lower()])
            self.lastDebugMsg = 'Copying file "%s" into "%s" took %.4f sec.' % (fname, new_fname, clock()-ti)
            return 0
        except:
            self.lastErrorMsg = 'Func CopyIntoNew: cannot find the file called "%s"!' % fname
            return -1


    def ExportFile(self, fname, path='', version=0, execute=False):
        '''
        Call one file from the briefcase. \n\
        If version is not null, that specific version is used. Else, it's the most recent version. \n\
        If execute is false, the file is simply exported into the specified path. Else, the file
        is executed from a temporary folder, or from the specified path, then the file is deleted. \n\
        '''
        ti = clock()
        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4

        # If version is a positive number, get that version.
        if version > 0:
            try:
                selected_version = self.c.execute('select raw from %s order by version desc where '
                    ' version=%s' % (filename, version)).fetchone()
            except:
                selected_version = False
            # If the version doesn't exist, exit.
            if not selected_version:
                self.lastErrorMsg = 'Func ExportFile: cannot find version "%i" for file "%s"!'\
                    % (version, fname)
                return -1
        # Else, get the latest version.
        else:
            try:
                selected_version = self.c.execute('select raw from %s order by version desc' %
                    filename).fetchone()
            except:
                selected_version = False
            # If the file doesn't exist, exit.
            if not selected_version:
                self.lastErrorMsg = 'Func ExportFile: cannot find the file called "%s"!' % fname
                return -1

        if path and not os.path.exists(path):
            self.lastErrorMsg = 'Func ExportFile: path "%s" doesn\'t exist!' % path
            return -1

        # If the path is specified, use it. Else, use a temp dir.
        if path:
            filename = path + '\\' + fname
        else:
            f = tempfile.mkdtemp('__', '__py')
            filename = f + '\\' + filename + os.path.splitext(fname)[1]
            del f

        w = open(filename, 'wb')
        w.write(self._restoreb(selected_version[0]))
        w.close() ; del w
        self.lastDebugMsg = 'Exporting file "%s" took %.4f sec.' % (fname, clock()-ti)

        # If execute, call the file, then delete it.
        if execute:
            os.system('"%s"&exit' % filename)
            os.remove(filename)
        # If not path, delete the temp folders.
        if not path:
            dirs = glob.glob(tempfile.gettempdir() + '\\' + '__py*__')
            for dir in dirs: shutil.rmtree(dir)
        return 0


    def ExportAll(self, path):
        '''
        Export all files into one folder. \n\
        Only the most recent version of each file is exported. \n\
        '''
        #
        ti = clock()
        #
        if not os.path.exists(path):
            self.lastErrorMsg = 'Func ExportAll: path "%s" doesn\'t exist!' % path
            return -1

        all_files = self.c.execute('select file from prv order by file').fetchall()[1:]
        for temp_file in all_files:
            md4 = MD4.new(temp_file[0])
            filename = 't'+md4.hexdigest()
            latest_version = self.c.execute('select raw from %s order by version desc' % filename).fetchone()
            filename = path + '\\' + temp_file[0]
            w = open(filename, 'wb')
            w.write(self._restoreb(latest_version[0]))
            w.close()

        self.lastDebugMsg = 'Exporting all files took %.4f sec.' % (clock()-ti)
        return 0


    def RenFile(self, fname, new_fname):
        '''
        Rename one file. This cannot be undone, so be careful. \n\
        '''
        ti = clock()
        if ('\\' in new_fname) or ('/' in new_fname) or (':' in new_fname) or ('*' in new_fname) \
            or ('?' in new_fname) or ('"' in new_fname) or ('<' in new_fname) or ('>' in new_fname) \
            or ('|' in new_fname):
            self.lastErrorMsg = 'Func RenFile: a filename cannot contain any of the following characters '\
                ' \\ / : * ? " < > |'
            return -1

        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4
        md4 = MD4.new( new_fname.lower() )
        new_filename = 't'+md4.hexdigest()
        del md4

        if self.c.execute('select * from prv where file="%s"' % (new_fname.lower())).fetchone():
            self.lastErrorMsg = 'Func RenFile: there is already a file called "%s"!' % new_fname
            return -1

        try:
            self.c.execute('alter table %s rename to %s' % (filename, new_filename))
            self.c.execute('update prv set file="%s" where file="%s"' % (new_filename, filename))
            self.lastDebugMsg = 'Renaming from "%s" into "%s" took %.4f sec.' % (fname, new_fname, clock()-ti)
            return 0
        except:
            self.lastErrorMsg = 'Func RenFile: cannot find the file called "%s"!' % fname
            return -1


    def DelFile(self, fname, version=0):
        '''
        If version is a positive number, only that version of the file is deleted. \n\
        Else, the entire table is dropped. \n\
        This cannot be undone, so be careful. \n\
        '''
        ti = clock()
        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4

        if version > 0:
            self.c.execute('delete from %s where version=%s' % (filename, version))
            self.c.execute('reindex %s' % filename)
            self.lastDebugMsg = 'Deleting file "%s" version "%i" took %.4f sec.' % (fname, version, clock()-ti)
        else:
            try:
                self.c.execute('drop table %s' % filename)
                self.c.execute('delete from prv where file="%s"' % fname.lower())
                self.conn.commit()
                self.lastDebugMsg = 'Deleting file "%s" took %.4f sec.' % (fname, clock()-ti)
                return 0
            except:
                self.lastErrorMsg = 'Func DelFile: cannot find the file called "%s"!' % fname
                return -1


    def GetProperties(self, fname):
        '''
        Returns a dictionary, containing the following key-value pairs : \n\
        fileName, firstFileDate, lastFileDate, firstFileUser, lastFileUser, versions. \n\
        If the file has 1 version, firstFileDate==lastFileDate and firstFileUser==lastFileUser. \n\
        On error, it returns -1. \n\
        '''
        ti = clock()
        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4

        try:
            firstFileDate = self.c.execute('select date from %s order by version asc' %
                filename).fetchone()[0]
            lastFileDate = self.c.execute('select date from %s order by version desc' %
                filename).fetchone()[0]
            firstFileUser = self.c.execute('select user from %s order by version asc' %
                filename).fetchone()[0]
            lastFileUser = self.c.execute('select user from %s order by version desc' %
                filename).fetchone()[0]
            versions = len( self.c.execute('select version from %s' % filename).fetchall() )
            #
            self.lastDebugMsg = 'Get properties for file "%s" took %.4f sec.' % (fname, clock()-ti)
            return {'fileName':fname, 'firstFileDate':firstFileDate, 'lastFileDate':lastFileDate,
                'firstFileUser':firstFileUser, 'lastFileUser':lastFileUser, 'versions':versions}
        except:
            self.lastErrorMsg = 'Func GetProperties: cannot find the file called "%s"!' % fname
            return -1


    def GetFileList(self):
        '''
        Returns a list with all the files from current Briefcase file. \n\
        Cannot have errors. \n\
        '''
        ti = clock()
        li = self.c.execute('select file from prv where file notnull order by file asc').fetchall()
        lf = []
        for elem in li:
            lf.append(elem[0])
        self.lastDebugMsg = 'Get file list took %.4f sec.' % (clock()-ti)
        return lf


#


if __name__ == '__main__':

    if not sys.argv[1:]:
        print('You must specify 3 arguments. Try "-h" parameter to see the complete list of commands.')
        exit(1)

    from optparse import OptionParser
    usage = "Usage: %prog --db <briefcase-file> --pwd <password> --command <arguments>"
    parser = OptionParser(usage=usage)

    parser.add_option("-b", "-q", "--brief", "--quiet", dest="verbose", action="store_false", default=False, help="Prints the version.")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True, help="Prints the version.")
    parser.add_option("--db", dest="database", help="The name of the briefcase file.")
    parser.add_option("--pwd", "--pass", dest="password", help="The password of the briefcase file.")
    parser.add_option("--addfile", action="store", nargs=2, help="-.")
    parser.add_option("--addmanyfiles", action="store", nargs=2, help="-.")
    parser.add_option("--copyintonew", action="store", nargs=3, help="-.")
    parser.add_option("--getversion", action="store", nargs=1, help="-.")
    parser.add_option("--exportfile", action="store", nargs=4, help="-.")
    parser.add_option("--exportall", action="store", nargs=1, help="-.")
    parser.add_option("--renfile", action="store", nargs=2, help="-.")
    parser.add_option("--delfile", action="store", nargs=2, help="-.")
    (options, args) = parser.parse_args()

    print( options )


# Eof()