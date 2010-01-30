
import sqlite3
from Crypto.Hash import MD4

conn = sqlite3.connect('Data.prv')
c = conn.cursor()

lines = c.execute('select * from prv').fetchall()
for line in lines:
    print( line )

labels = c.execute('select * from labels').fetchall()
for label in labels:
    print( label )

print
md4 = MD4.new( lines[1][0] )
filename = 't'+md4.hexdigest()
print c.execute('select * from %s' % filename).fetchone()

print
md4 = MD4.new( lines[2][0] )
filename = 't'+md4.hexdigest()
print c.execute('select * from %s' % filename).fetchone()
