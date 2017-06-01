import numpy as np
import pandas as pd
from konlpy.tag import Twitter
import gensim
from sklearn.decomposition import PCA
import mysql.connector as msc

def tokenize(doc):
    result = list()
    pos_tagger = Twitter()
    for s in pos_tagger.pos(doc, norm=True, stem=True):
        if s[1] in ['Noun', 'Verb', 'Adjective', 'Adverb']:
            result.append(s[0])
    return result


def make_model(db_name_1, db_name_2 = None, inclination=None):
    config = {'host': ***REMOVED***,
              'port': ***REMOVED***,
              'user': ***REMOVED***,
              'password': ***REMOVED***,
              'database': ***REMOVED***}
    conn = msc.connect(**config)
    qry = conn.cursor(buffered=True)

    if inclination is not None:
        query = "SELECT Contents FROM %s WHERE Inclination = %d" % (db_name_1, inclination)
    else:
        query = "SELECT Contents FROM %s" % db_name_1

    qry.execute(query)
    row = qry.fetchone()

    train_docs = list()
    while row is not None:
        try:
            train_docs.append(tokenize(row[0]))
        except Exception as e:
            print(e)
            continue
        row = qry.fetchone()

    if db_name_2 is not None:
        if inclination is not None:
            query = "SELECT Contents FROM %s WHERE Inclination = %d" % (db_name_2, inclination)
        else:
            query = "SELECT Contents FROM %s" % db_name_2

        qry.execute(query)
        row = qry.fetchone()

        while row is not None:
            try:
                train_docs.append(tokenize(row[0]))
            except Exception as e:
                print(e)
                continue
            row = qry.fetchone()

    model = gensim.models.Word2Vec(train_docs, size=3)

    if db_name_2 is None:
        if inclination is None:
            model.save('%s.model' % db_name_1)
        else:
            model.save('%s_%d.model' % (db_name_1, inclination))
    else:
        if inclination is None:
            model.save('%s_%s.model' % (db_name_1, db_name_2))
        else:
            model.save('%s_%s_%d.model' % (db_name_1, db_name_2, inclination))



def vectorize(vocab_list, db_name_1, db_name_2 = None):
    if db_name_2 is None:
        model = gensim.models.Word2Vec.load('../../word2vec/%s.model' % db_name_1)
    else:
        model = gensim.models.Word2Vec.load('../../word2vec/%s_%s.model' % (db_name_1, db_name_2))

    result = list()
    for word in vocab_list:
        try:
            result.append((model[word[0]], model.most_similar(word[0])))
        except:
            result.append(([0,0,0], [('error',0),('error',0),('error',0),('error',0),('error',0)]))
    return result


# Do not use
def pca_projection(word2vec):
    pca = PCA(n_components=3)

    pca.fit(word2vec)
    projected_vec = pca.transform(word2vec)

    result = list()
    for vec in projected_vec:
        result.append([format(vec[0], '.4f'), format(vec[1], '.4f'), format(vec[2], '.4f')])

    return result


if __name__ == '__main__':
    print("twitter_tweet")
    make_model(db_name_1="twitter_tweet")
    print("twitter_tweet_1")
    make_model(db_name_1="twitter_tweet", inclination=1)
    print("twitter_tweet_2")
    make_model(db_name_1="twitter_tweet", inclination=2)

    print("twitter_reply")
    make_model(db_name_1="twitter_reply")
    print("twitter_reply_1")
    make_model(db_name_1="twitter_reply", inclination=1)
    print("twitter_reply_2")
    make_model(db_name_1="twitter_reply", inclination=2)

    # print("twitter_tweet & reply")
    # make_model(db_name_1="twitter_tweet", db_name_2="twitter_reply")
    # print("twitter_tweet & reply_1")
    # make_model(db_name_1="twitter_tweet", db_name_2="twitter_reply", inclination=1)
    # print("twitter_tweet & reply_2")
    # make_model(db_name_1="twitter_tweet", db_name_2="twitter_reply", inclination=2)