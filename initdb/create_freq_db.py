import mysql.connector as msc
from collections import Counter
from NLP import *

lab={'host':***REMOVED***,
        'port':***REMOVED***,
        'user':***REMOVED***,
        'password':***REMOVED***,
        'database':***REMOVED***}

conn = msc.connect(**lab)
conn2 = msc.connect(**lab)
qry = conn.cursor(buffered=True)
qry2 = conn2.cursor(buffered=True)

nlp = NLP_Engine()

qry.execute("select * from politician where Inclination=1")
row = qry.fetchone()
while row is not None:
    qry2.execute("SELECT Contents FROM twitter_reply WHERE Origin_Screen_Name='%s'" % row[1])
    row2 = qry2.fetchone()

    word_list = list()
    while row2 is not None:
        result = nlp.ExtractPOS(row2[0], 3)
        for word, pos in result:
            if pos in list(['Noun', 'Vern', 'Adjective', 'Adverb']):
                word_list.append(word)
            else:
                continue
        row2 = qry2.fetchone()
    conn2.commit()

    word_freq = Counter(word_list)
    word_freq = word_freq.most_common()
    for tpl in word_freq:
        qry2.execute("INSERT INTO right_reply_frequency VALUE('%s', '%s', %d);" % (row[1], tpl[0], tpl[1]))
    conn2.commit()

    print("%s is Done!" % row[1])
    row = qry.fetchone()

qry.close()
conn.close()
qry2.close()
conn2.close()