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
        Valid passwords : a string or a null value. \n\
        One SQLITE3 file for each Briefcase instance. \n\
        '''
        #
        self.database = str(database)
        self.verbose = 2
        #
        if os.path.exists(self.database):
            exists_db = True
        else:
            exists_db = False
        #
        self.conn = sqlite3.connect(self.database)
        self.c = self.conn.cursor()
        self.pwd = password
        #

        # If password is a string or unicode, get the hash.
        if type(password) == type('') or type(password) == type(u''):
            md4 = MD4.new(password)
            self.gpwd_hash = md4.hexdigest()
        # If password is null in some way, hash must be also null.
        else:
            password = None
            self.gpwd_hash = None

        if exists_db:
            # Test user password versus database password.
            if self.gpwd_hash != self.c.execute('select pwd from prv').fetchone()[0]:
                raise Exception('The password is INCORRECT! You will not be able to decrypt any data!')
        else:
            # Create prv table with passwords and original names of the files.
            self.c.execute('create table labels (label TEXT unique, files TEXT)')
            self.c.execute('create table prv (file TEXT unique, pwd BLOB, labels TEXT)')
            self.c.execute('insert into prv (file, pwd) values (?,?)', [None, self.gpwd_hash])
            self.conn.commit()
        #


    def _normalize_16(self, L):
        return 'X' * ((((L/16)+1)*16)-L)


    def _transformb(self, bdata, pwd=''):
        '''
        Transforms any binary data into ready-to-write SQL information. \n\
        '''
        vCompressed = zlib.compress(bdata,9)
        # If password is null in some way, do not encrypt.
        if not pwd:
            return buffer(vCompressed)
        # If password has default value.
        elif pwd == 1:
            # If default value is null, do not encrypt.
            if not self.pwd:
                return buffer(vCompressed)
            else:
                pwd = self.pwd + self._normalize_16(len(self.pwd))
        # If password is provided, normalize it to 16 characters.
        else:
            pwd += self._normalize_16(len(pwd))
        # Now crypt and return.
        crypt = AES.new(pwd)
        vCrypt = crypt.encrypt(vCompressed + self._normalize_16(len(vCompressed)))
        return buffer(vCrypt)


    def _restoreb(self, bdata, pwd=''):
        '''
        Restores binary data from SQL information. \n\
        '''
        # If password is null in some way, do not encrypt.
        if not pwd:
            return zlib.decompress(bdata)
        # If password has default value.
        elif pwd == 1:
            # If default value is null, do not encrypt.
            if not self.pwd:
                return zlib.decompress(bdata)
            else:
                pwd = self.pwd + self._normalize_16(len(self.pwd))
        # If password is provided, normalize it to 16 characters.
        else:
            pwd += self._normalize_16(len(pwd))
        # Now decrypt and return.
        crypt = AES.new(pwd)
        vCompressed = crypt.decrypt(bdata)
        return zlib.decompress(vCompressed)


    def _log(self, level, msg):
        '''
        Prints debug and error messages. \n\
        '''
        if self.verbose <= 0:
            # Don't print anything.
            return 0
        elif self.verbose == 1:
            # Only errors are printed.
            if level == 2:
                print( msg )
                return 1
        elif self.verbose == 2:
            # All messages are printed.
            print( msg )
            return 2


    def SetLabels(self, fname, labels):
        '''
        Set labels/ tags/ keywords for one filename. Labels can be used to sort and filter files. \n\
        Labels must be a ";"-separated string, a list, or a tuple. Any character excepting ";" can be used.\n\
        '''
        ti = clock()

        if not labels:
            self.c.execute('update prv set labels=? where file=?', ['', fname.lower()])
            return 0

        if type(labels) == type('') or type(labels) == type(u''):
            lLabels = sorted([s.strip() for s in labels.split(';')])
            sLabels = ';'.join(lLabels)
        elif type(labels) == type([0,0]) or type(labels) == type((0,0)):
            lLabels = sorted([s.strip() for s in labels])
            sLabels = ';'.join(lLabels)
        else:
            self._log(2, 'Func SetLabels: invalid type for the label! It must be : string, unicode, '
                'list, or tuple. You provided type "%s".' % type(label))
            return -1

        # If file doesn't exist in database, exit.
        if not self.c.execute('select file from prv where file=?', [fname.lower()]).fetchone():
            self._log(2, 'Func SetLabels: file "%s" doesn\'t exist!' % fname)
            return -1

        for label in lLabels:
            # Save old "list of files" from table. In fact it's a string.
            files = self.c.execute('select files from labels where label=?', [label]).fetchone()
            if files:
                # Add the new file to the list of files.
                self.c.execute('insert or replace into labels (label, files) values (?,?)',
                    [label, files[0]+';'+fname])
            else:
                # Add the new file for the first time.
                self.c.execute('insert into labels (label, files) values (?,?)', [label, fname])

        # Updata labels in PRV.
        self.c.execute('update prv set labels=? where file=?', [sLabels, fname.lower()])
        self.conn.commit()
        self._log(1, 'Setting labels for file "%s" took %.4f sec.' % (fname, clock()-ti))
        return 0


    def AddFile(self, filepath, password=1, labels='', versionable=True):
        '''
        If file doesn't exist in database, create the file. If file exists, add another row. \n\
        Table name is "t" + MD4 Hexdigest of the file name (lower case). \n\
        Each row contains : Version, Raw-data, Hash of original data, Date and Time, User Name. \n\
        Raw-data is : original binary data -> compressed -> crypted. \n\
        Versionable=False checks if the file is in the database. If it is, an error is raised
        and the file is not added. \n\
        '''
        ti = clock()
        fpath = filepath.lower()

        if not os.path.exists(fpath):
            self._log(2, 'Func AddFile: file path "%s" doesn\'t exist!' % filepath)
            return -1

        # If password is a string or unicode, get the hash.
        if type(password) == type('') or type(password) == type(u''):
            md4 = MD4.new(password)
            pwd_hash = md4.hexdigest()
        # If password has default value.
        elif password == 1:
            pwd_hash = self.gpwd_hash
        # If password is null in some way, hash must be also null.
        else:
            password = None
            pwd_hash = None

        md4 = MD4.new( os.path.split(fpath)[1] )
        filename = 't'+md4.hexdigest()
        del md4

        old_pwd_hash = self.c.execute('select pwd from prv where file="%s"' % fpath).fetchone()

        # If file exists in DB and user provided a password.
        if old_pwd_hash and password:
            old_pwd_hash = old_pwd_hash[0]
            # If password from user is differend from password in DB, exit.
            if old_pwd_hash != pwd_hash:
                self._log(2, 'Func AddFile: The password is INCORRECT! You will not be able to '\
                    'decrypt/ encrypt any data!')
                return -1
        # If file exists in DB but no password was provided.
        elif old_pwd_hash:
            # ... and versionable is False, exit.
            if not versionable:
                self._log(2, 'Func AddFile: you selected versionable=False, so no new version '\
                    'will be added!')
                return -1

        self.c.execute('create table if not exists %s (version integer primary key asc, raw BLOB,'\
            'hash TEXT, size INTEGER, date TEXT, user TEXT)' % filename)

        # Get file size.
        size = os.path.getsize(filepath)
        # Read and transform all binary data.
        f = open(filepath, 'rb').read()
        # This is the raw data.
        raw = self._transformb(f, password)
        md4 = MD4.new(f)
        # This is the hash of the original file.
        hash = md4.hexdigest()
        del f, md4

        # Check if the new file is identical with the latest version.
        old_hash = self.c.execute('select hash from %s order by version desc' % filename).fetchone()
        if old_hash and hash == old_hash[0]:
            self._log(2, 'Func AddFile: file "%s" is IDENTICAL with the version stored in the '\
                'database!' % os.path.split(fpath)[1])
            return -1

        self.c.execute(('insert into %s (raw, hash, size, date, user) values (?,?,?,?,?)' % filename),
            [raw, hash, size, strftime("%Y-%b-%d %H:%M:%S"), os.getenv('USERNAME')])

        # If password is None, or password is False.
        if not password:
            self.c.execute('insert or ignore into prv (pwd, file) values (?,?)', [password, os.path.split(fpath)[1]])
        # If password is provided by user, insert its hash in prv table.
        else:
            self.c.execute('insert or ignore into prv (pwd, file) values (?,?)', [pwd_hash, os.path.split(fpath)[1]])

        # Set the labels...
        self.SetLabels(os.path.split(fpath)[1], labels)

        # Everything is fine, save.
        self.conn.commit()

        ver_max = self.c.execute('select version from %s order by version desc' % filename).fetchone()
        self._log(1, 'Adding file "%s" version "%i" took %.4f sec.' % (filepath, ver_max[0], clock()-ti))
        return 0


    def AddManyFiles(self, pathregex, password=1, labels='', versionable=True):
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
            self._log(2, 'Func AddManyFiles: path "%s" doesn\'t exist!' % path)
            return -1

        files = glob.glob(pathreg)

        if not len(files):
            self._log(2, 'Func AddManyFiles: there are no files to match "%s"!' % pathregex)
            return -1

        for file in files:
            self.AddFile(file, password, labels, versionable)

        self._log(1, 'Added %i files in %.4f sec.' % (len(files), clock()-ti))
        return 0


    def CopyIntoNew(self, fname, version, new_fname):
        '''
        Copy one version of one file, into a new file, that will have version 1. \n\
        The password will be the same as in the original file. \n\
        '''
        ti = clock()
        if ('\\' in new_fname) or ('/' in new_fname) or (':' in new_fname) or ('*' in new_fname) \
            or ('?' in new_fname) or ('"' in new_fname) or ('<' in new_fname) or ('>' in new_fname) \
            or ('|' in new_fname):
            self._log(2, 'Func CopyIntoNew: a file name cannot contain any of the following '\
                'characters  \\ / : * ? " < > |')
            return -1

        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4
        md4 = MD4.new( new_fname.lower() )
        new_filename = 't'+md4.hexdigest()
        del md4

        if version < 0 : version = 0

        # If new file name already exists, exit.
        if self.c.execute('select file from prv where file="%s"' % (new_fname.lower())).fetchone():
            self._log(2, 'Func CopyIntoNew: there is already a file called "%s"!' % new_fname)
            return -1

        # Try to extract specified version.
        try:
            self.c.execute('select version from %s' % filename).fetchone()
        except:
            self._log(2, 'Func CopyIntoNew: there is no such file called "%s"!' % fname)
            return -1

        # If version was specified, get that version.
        if version:
            data = self.c.execute('select raw, hash, size from %s where version=%i' % (filename, version)
                ).fetchone()
        # Else, get the latest version.
        else:
            data = self.c.execute('select raw, hash, size from %s order by version desc' % filename
                ).fetchone()

        self.c.execute('create table %s (version integer primary key asc, raw BLOB, hash TEXT,'
            'size INTEGER, date TEXT, user TEXT)' % new_filename)
        self.c.execute(('insert into %s (raw, hash, size, date, user) values (?,?,?,?,?)' % new_filename),
            [data[0], data[1], data[2], strftime("%Y-%b-%d %H:%M:%S"), os.getenv('USERNAME')])

        # Use original password and labels of file.
        more = self.c.execute('select pwd, labels from prv where file=?', [fname.lower()]).fetchone()

        self.c.execute('insert into prv (file, pwd, labels) values (?,?,?)', (new_fname.lower(),)+more)
        self.conn.commit()

        self._log(1, 'Copying file "%s" into "%s" took %.4f sec.' % (fname, new_fname, clock()-ti))
        return 0


    def ExportFile(self, fname, password=1, version=0, path='', execute=False):
        '''
        Call one file from the briefcase. \n\
        If version is not null, that specific version is used. Else, the most recent version is used. \n\
        If execute is false, the file is simply exported into the specified path. Else, the file
        is executed from a temporary folder, or from the specified path, then the file is deleted. \n\
        '''
        ti = clock()
        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4

        if version < 0 : version = 0

        if path and not os.path.exists(path):
            self._log(2, 'Func ExportFile: path "%s" doesn\'t exist!' % path)
            return -1

        # If version is a positive number, get that version.
        if version > 0:
            try:
                selected_version = self.c.execute('select raw from %s where version=%s' %
                    (filename, version)).fetchone()
            except:
                self._log(2, 'Func ExportFile: cannot find version "%i" for file "%s"!' %\
                    (version, fname))
                return -1
        # Else, get the latest version.
        else:
            try:
                selected_version = self.c.execute('select raw from %s order by version desc' %
                    filename).fetchone()
            except:
                self._log(2, 'Func ExportFile: cannot find the file called "%s"!' % fname)
                return -1

        # If the path is specified, use it. Else, use a temp dir.
        if path:
            filename = path + '\\' + fname
        else:
            f = tempfile.mkdtemp('__', '__py')
            filename = f + '\\' + filename + os.path.splitext(fname)[1]
            del f

        # Get file password hash. It can be None, (Zero), or (some hash string).
        old_pwd_hash = self.c.execute('select pwd from prv where file="%s"' % fname.lower()).fetchone()
        if old_pwd_hash:
            old_pwd_hash = old_pwd_hash[0]

        # If password is a string or unicode, get the hash.
        if type(password) == type('') or type(password) == type(u''):
            md4 = MD4.new(password)
            pwd_hash = md4.hexdigest()
        # If password has default value.
        elif password == 1:
            password = self.pwd
            pwd_hash = self.gpwd_hash
        # If password is null in some way, hash must be also null.
        else:
            password = None
            pwd_hash = None

        # If provided password != stored password...
        if old_pwd_hash != pwd_hash:
            self._log(2, 'Func ExportFile: Password for file "%s" is INCORRECT! You will not be '\
                'able to decrypt any data!' % fname)
            # Delete any leftover temp files.
            if not path:
                dirs = glob.glob(tempfile.gettempdir() + '\\' + '__py*__')
                try:
                    for dir in dirs: shutil.rmtree(dir)
                except: pass
            return -1

        w = open(filename, 'wb')
        w.write(self._restoreb(selected_version[0], password))
        w.close() ; del w
        self._log(1, 'Exporting file "%s" took %.4f sec.' % (fname, clock()-ti))

        # If execute, call the file, then delete it.
        if execute:
            os.system('"%s"&exit' % filename)
            os.remove(filename)
        # If not path, delete all temp folders.
        if not path:
            dirs = glob.glob(tempfile.gettempdir() + '\\' + '__py*__')
            try:
                for dir in dirs: shutil.rmtree(dir)
            except: pass
        return 0


    def ExportAll(self, path, password=1):
        '''
        Export all files into one folder. \n\
        Only the most recent version of each file is exported. \n\
        '''
        #
        ti = clock()
        #
        if not os.path.exists(path):
            self._log(2, 'Func ExportAll: path "%s" doesn\'t exist!' % path)
            return -1

        # If password is a string or unicode, get the hash.
        if type(password) == type('') or type(password) == type(u''):
            md4 = MD4.new(password)
            pwd_hash = md4.hexdigest()
        # If password has default value.
        elif password == 1:
            password = self.pwd
            pwd_hash = self.gpwd_hash
        # If password is null in some way, hash must be also null.
        else:
            password = None
            pwd_hash = None

        all_files = self.c.execute('select pwd, file from prv order by file').fetchall()[1:]

        # Temp_file[0] = pwd, Temp_file[1] = fname.
        for temp_file in all_files:
            # If provided password != stored password...
            if temp_file[0] != pwd_hash:
                self._log(2, 'Func ExportAll: Password for file "%s" is INCORRECT! You will not be'\
                    ' able to decrypt any data!' % temp_file[1])
                continue

            # At this point, password is correct.
            fname = path + '\\' + temp_file[1]
            w = open(fname, 'wb')
            md4 = MD4.new(temp_file[1])
            filename = 't'+md4.hexdigest()
            latest_version = self.c.execute('select raw from %s order by version desc' % filename).fetchone()
            w.write(self._restoreb(latest_version[0], password))
            w.close()
            self._log(2, 'Func ExportAll: File "%s" exported successfully.' % temp_file[1])

        self._log(1, 'Exporting all files took %.4f sec.' % (clock()-ti))
        return 0


    def RenFile(self, fname, new_fname):
        '''
        Rename one file. This cannot be undone, so be careful. \n\
        '''
        ti = clock()
        if ('\\' in new_fname) or ('/' in new_fname) or (':' in new_fname) or ('*' in new_fname) \
            or ('?' in new_fname) or ('"' in new_fname) or ('<' in new_fname) or ('>' in new_fname) \
            or ('|' in new_fname):
            self._log(2, 'Func RenFile: a filename cannot contain any of the following characters '\
                ' \\ / : * ? " < > |')
            return -1

        md4 = MD4.new( fname.lower() )
        filename = 't'+md4.hexdigest()
        del md4
        md4 = MD4.new( new_fname.lower() )
        new_filename = 't'+md4.hexdigest()
        del md4

        if self.c.execute('select * from prv where file="%s"' % (new_fname.lower())).fetchone():
            self._log(2, 'Func RenFile: there is already a file called "%s"!' % new_fname)
            return -1

        try:
            self.c.execute('alter table %s rename to %s' % (filename, new_filename))
            self.c.execute('update prv set file = ? where file = ?', [new_fname, fname])
            self.conn.commit()
            self._log(1, 'Renaming from "%s" into "%s" took %.4f sec.' % (fname, new_fname, clock()-ti))
            return 0
        except:
            self._log(2, 'Func RenFile: cannot find the file called "%s"!' % fname)
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
            self.conn.commit()
            self._log(1, 'Deleting file "%s" version "%i" took %.4f sec.' % (fname, version, clock()-ti))
            return 0
        else:
            try:
                self.c.execute('drop table %s' % filename)
                self.c.execute('delete from prv where file="%s"' % fname.lower())
                self.conn.commit()
                self._log(1, 'Deleting file "%s" took %.4f sec.' % (fname, clock()-ti))
                return 0
            except:
                self._log(2, 'Func DelFile: cannot find the file called "%s"!' % fname)
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
            # Size.
            firstFileSize = self.c.execute('select size from %s order by version asc' %
                filename).fetchone()[0]
            lastFileSize = self.c.execute('select size from %s order by version desc' %
                filename).fetchone()[0]
            firstFileDate = self.c.execute('select date from %s order by version asc' %
                filename).fetchone()[0]
            lastFileDate = self.c.execute('select date from %s order by version desc' %
                filename).fetchone()[0]
            firstFileUser = self.c.execute('select user from %s order by version asc' %
                filename).fetchone()[0]
            lastFileUser = self.c.execute('select user from %s order by version desc' %
                filename).fetchone()[0]
            labels = self.c.execute('select labels from prv where file="%s"' %
                fname.lower()).fetchone()[0]
            versions = len( self.c.execute('select version from %s' % filename).fetchall() )
            #
            self._log(1, 'Get properties for file "%s" took %.4f sec.' % (fname, clock()-ti))
            return {'fileName':fname, 'internFileName':filename,
                'firstFileSize':firstFileSize, 'lastFileSize':lastFileSize,
                'firstFileDate':firstFileDate, 'lastFileDate':lastFileDate,
                'firstFileUser':firstFileUser, 'lastFileUser':lastFileUser,
                'labels':labels, 'versions':versions}
        except:
            self._log(2, 'Func GetProperties: cannot find the file called "%s"!' % fname)
            return -1


    def GetFileList(self, sort='', filter=''):
        '''
        Returns a list with all the files from current Briefcase file. \n\
        Cannot have errors. \n\
        '''
        ti = clock()
        li = self.c.execute('select file from prv where file notnull order by file asc').fetchall()
        lf = []
        for elem in li:
            lf.append(elem[0])
        self._log(1, 'Get file list took %.4f sec.' % (clock()-ti))
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