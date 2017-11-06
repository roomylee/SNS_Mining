from NLP import *
from config import db_config

lab = db_config.lab_server

conn = msc.connect(**lab)
conn2 = msc.connect(**lab)
qry = conn.cursor(buffered=True)
qry2 = conn2.cursor(buffered=True)

nlp = NLP_Engine()

qry.execute("select * from politician where Inclination=2")
row = qry.fetchone()
while row is not None:
    qry2.execute("SELECT Contents FROM twitter_reply WHERE Origin_Screen_Name='%s'" % row[1])
    row2 = qry2.fetchone()

    word_list = list()
    while row2 is not None:
        result = nlp.ExtractPOS(row2[0])
        for word, pos in result:
            if pos in list(['Noun', 'Verb', 'Adjective', 'Adverb']):
                if word not in ['꼭','더'] and len(word) < 2:
                    continue
                elif word in ['하다','있다','이다','되다','가다',
                              '않다','없다','오다','자다','말다',
                              '대다','돼다','되어다',]:
                    continue
                word_list.append(word)
            else:
                continue
        row2 = qry2.fetchone()
    conn2.commit()

    word_freq = Counter(word_list)
    word_freq = word_freq.most_common()
    for tpl in word_freq:
        qry2.execute("INSERT INTO left_reply_frequency VALUE('%s', '%s', %d);" % (row[1], tpl[0], tpl[1]))
    conn2.commit()

    print("%s is Done!" % row[1])
    row = qry.fetchone()

qry.close()
conn.close()
qry2.close()
conn2.close()