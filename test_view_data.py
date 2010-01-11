
import sqlite3
from Crypto.Hash import MD4

conn = sqlite3.connect('Data.prv')
c = conn.cursor()

for line in c.execute('select * from prv').fetchmany(8):
    if not line[0] : file1 = line[1]
    print( line )

print
md4 = MD4.new( file1 )
filename = 't'+md4.hexdigest()

for line in c.execute('select * from %s' % filename).fetchmany(5):
    print( line )
