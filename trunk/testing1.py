#! /usr/local/bin/python
# -*- coding: latin-1 -*-

'''
Testing strategy :

-	Create a new briefcase file with password;
-	Try to open the briefcase with as many wrong passwords as possible, the file should NOT open;
-	Add a file with pwd and try to open it with many wrong pwds, the file should NOT open;
-	Add a few hundred files and check their number;
-	Decrypt the files just to test if they are all intact;
-	Add many versions for a few files, export the versions to test if they are intact;
-	Copy a few files and check identity and check the number of files;
-	Export a few "cloned" files and check with the original;
-	Rename a few files and check the number of files;
-	Export a few renamed files and check with the original;

'''

import os, sys, shutil
from glob import glob
from random import randrange

from Crypto.Hash import MD5
from Crypto.Random import get_random_bytes

from briefcase import Briefcase

#

def RandFile(fname='file.rnd', append=False):
	# Returns a random piece of text.
	words = randrange(1, 99)
	# Join with space or newline.
	if randrange(1, 9) % 2:
		space = ' ' * randrange(3, 19)
	else:
		space = '\n' * randrange(3, 19)
	txt = []
	for i in range(words):
		# Word length.
		L = randrange(1, 99)
		txt.append(get_random_bytes(L))
	if append:
		f = open(fname, 'a')
	else:
		f = open(fname, 'wb')
	f.write(space.join(txt))
	f.close()

def RandPassword():
	# Returns a random password between 1 and 32.
	L = randrange(1, 32)
	pwd = []
	for i in range(L):
		# From 'space' to '~'.
		pwd.append( chr(randrange(32, 126)) )
	return ''.join(pwd)

#
TESTS = 10
TEST_PASS = True
#

# Delete temp folders.
try: shutil.rmtree(os.getcwd()+'/temp_test')
except: pass
try: shutil.rmtree(os.getcwd()+'/temp_test_exp')
except: pass
# Re-create temp folders.
os.mkdir(os.getcwd()+'/temp_test')
os.mkdir(os.getcwd()+'/temp_test_exp')
# Remove old briefcase file.
try: os.remove('test.prv')
except: pass

# Create Briefcase instance with password.
b = Briefcase('test.prv', 'default password')
del b

print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
print('Test:: briefcase with wrong passwords.')
print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')

for i in range(5):
	pwd_len = randrange(1, 9)
	rnd_pwd = get_random_bytes(pwd_len)
	try:
		Briefcase('test.prv', rnd_pwd)
		print('This is wrong man, i cracked the briefcase with pwd: `%s` !' % rnd_pwd)
		TEST_PASS = False
	except Exception, e:
		pass

print('Ok, opening the database again...\n')

b = Briefcase('test.prv', 'default password')

print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
print('Test:: adding random files in the briefcase, with default password.')
print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')

for i in range(TESTS):
	# File names...
	short = 'file%i.rnd' % i
	fname = os.getcwd()+'/temp_test/'+short
	ename = os.getcwd()+'/temp_test_exp/'+short
	# Create a random file
	RandFile(fname)
	# Add the file with the default DB password
	b.AddFile(fname)
	# Export the file
	b.ExportFile(short, path=os.getcwd()+'/temp_test_exp')

	# Check identity
	if MD5.new(open(fname, 'rb').read()).digest() != MD5.new(open(ename, 'rb').read()).digest():
		print('This is wrong man, file `%s` is not the same after import/ export!' % fname)
		TEST_PASS = False

	b.DelFile(short)
	print

b.Cleanup()

print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
print('Test:: adding random files in the briefcase, with user password.')
print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')

for i in range(TESTS):
	# File names...
	short = 'file%i.rnd' % i
	fname = os.getcwd()+'/temp_test/'+short
	ename = os.getcwd()+'/temp_test_exp/'+short
	pwd = RandPassword()
	# Create a random file
	RandFile(fname)
	# Add the file with the default DB password
	b.AddFile(fname, pwd)
	# Export the file
	b.ExportFile(short, pwd, path=os.getcwd()+'/temp_test_exp')

	# Check identity
	if MD5.new(open(fname, 'rb').read()).digest() != MD5.new(open(ename, 'rb').read()).digest():
		print('This is wrong man, file `%s` is not the same after import/ export!' % fname)
		TEST_PASS = False

	for i in range(3):
		rnd_pwd = RandPassword()
		r = b.ExportFile(short, rnd_pwd, path=os.getcwd()+'/temp_test_exp')
		if r != -1:
			print('This is wrong man, i cracked the file with pwd: `%s` !' % rnd_pwd)
			TEST_PASS = False

	b.DelFile(short)
	print

b.Cleanup()

print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
print('Test:: adding versions for one file, with default password.')
print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')

short = 'file.rnd'

for i in range(TESTS):
	# File name...
	fname = os.getcwd()+'/temp_test/'+short
	ename = os.getcwd()+'/temp_test_exp/'+short
	# Append in the random file
	RandFile(fname, True)
	# Add the file with the default DB password
	b.AddFile(fname)
	# Export the file
	b.ExportFile(short, path=os.getcwd()+'/temp_test_exp')

	# Check identity
	if MD5.new(open(fname, 'rb').read()).digest() != MD5.new(open(ename, 'rb').read()).digest():
		print('This is wrong man, file `%s` is not the same after import/ export!' % fname)
		TEST_PASS = False

	del fname, ename
	print

nrFiles = b.Info()['numberOfFiles']
if nrFiles == 1:
	print('There should be `%i` file in the briefcase... Ok.' % nrFiles)
else:
	print('This is wrong man, there should be only 1 file in the briefcase!')
	TEST_PASS = False

print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
print('Test:: cloning one file many times and check identity.')
print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')

for i in range(TESTS):
	short_clone = 'file%i.rnd' % i
	fname = os.getcwd()+'/temp_test/'+short
	ename = os.getcwd()+'/temp_test_exp/'+short_clone
	# Clone file
	b.CopyIntoNew(short, 0, short_clone)
	# Export the file
	b.ExportFile(short_clone, path=os.getcwd()+'/temp_test_exp')

	# Check identity
	if MD5.new(open(fname, 'rb').read()).digest() != MD5.new(open(ename, 'rb').read()).digest():
		print('This is wrong man, file `%s` is not the same after import/ export!' % fname)
		TEST_PASS = False

	b.DelFile(short_clone)
	del fname, ename
	print

nrFiles = b.Info()['numberOfFiles']
if nrFiles == 1:
	print('There should be `%i` file in the briefcase... Ok.' % nrFiles)
else:
	print('This is wrong man, there should be only 1 file in the briefcase!')
	TEST_PASS = False

b.DelFile(short)
b.Cleanup()

print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
print('Test:: renaming files and check identity.')
print('# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')

short = 'file.rnd'

for i in range(TESTS):
	# File names...
	short_ren = 'file%i.rnd' % i
	fname = os.getcwd()+'/temp_test/'+short
	ename = os.getcwd()+'/temp_test_exp/'+short_ren
	# Create a random file
	RandFile(fname)
	# Add the file with the default DB password
	b.AddFile(fname)
	# Rename the file
	b.RenFile(short, short_ren)
	# Export the file
	b.ExportFile(short_ren, path=os.getcwd()+'/temp_test_exp')

	# Check identity
	if MD5.new(open(fname, 'rb').read()).digest() != MD5.new(open(ename, 'rb').read()).digest():
		print('This is wrong man, file `%s` is not the same after import/ export!' % fname)
		TEST_PASS = False

	print

nrFiles = b.Info()['numberOfFiles']
if nrFiles == TESTS:
	print('There should be `%i` file in the briefcase... Ok.\n' % nrFiles)
else:
	print('This is wrong man, there should be %i file in the briefcase!\n' % TESTS)
	TEST_PASS = False

for i in range(TESTS):
	short_ren = 'file%i.rnd' % i
	b.DelFile(short_ren)

print
b.Cleanup()

#

if TEST_PASS:
	print('All tests passed! Whee!\n')
else:
	print('Testing failed!\n')

# Eof()
