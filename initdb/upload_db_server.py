import mysql.connector as msc
from config import db_config

lab = db_config.lab_server

local = db_config.local


conn = msc.connect(**local)
qry = conn.cursor(buffered=True)

l_conn = msc.connect(**lab)
l_qry = l_conn.cursor(buffered=True)

qry.execute("select * from twitter_retweet")
row = qry.fetchone()
while row is not None:
    try:
        l_qry.execute("INSERT ignore SNS_Mining.twitter_retweet VALUE('%s','%s',%d,'%s','%s','%s',%d,%d,'%s','%s','%s')" \
                 % (row[0],row[1],row[2],row[3],row[4],row[5].replace("'","''"),row[6],row[7],row[8],row[9],row[10]))
        l_conn.commit()

        row = qry.fetchone()
    except:
        print(row)
        break;

l_qry.close()
l_conn.close()
qry.close()
conn.close()
