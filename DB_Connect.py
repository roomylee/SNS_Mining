import mysql.connector as msc

config = {
    'user':***REMOVED***,
    'password':***REMOVED***,
    'database':***REMOVED***,
}


db = msc.connect(**config)
qry = db.cursor(buffered=True)
qry.execute("select * from twitter")
print(qry.fetchall())
qry.close()
db.close()