#-*- coding: utf-8 -*-

from konlpy.tag import *
import mysql.connector as msc
import pandas as pd
import operator
from collections import Counter

class NLP_Engine:
    def __init__(self):
        #self.engines = [Kkma(), Hannanum(), Mecab(), Twitter()]
        self.engines = [Kkma(), Hannanum(), None, Twitter()]

    def ExtractNoun(self, sentence, eng):
        noun = self.engines[eng].nouns(sentence)
        return noun

    def ExtractPOS(self, sentence, eng):
        POS = self.engines[eng].pos(sentence, norm=True, stem=True)
        return POS

def get_frequent_words(people_list, table_list):
    config = {'host': ***REMOVED***,
              'port': ***REMOVED***,
              'user': ***REMOVED***,
              'password': ***REMOVED***,
              'database': ***REMOVED***}
    conn = msc.connect(**config)
    qry = conn.cursor(buffered=True)

    freq_dict = {}
    for t in table_list:
        query = "SELECT * FROM %s WHERE " % t
        flag = False
        for p in people_list:
            if flag is False:
                flag = True
            else:
                query += " or "
            query += "Screen_Name='%s'" % p
        query += ";"
        qry.execute(query)
        row = qry.fetchone()
        while row is not None:
            if row[1] in freq_dict:
                freq_dict[row[1]] = freq_dict[row[1]] + int(row[2])
            else:
                freq_dict[row[1]] = int(row[2])
            row = qry.fetchone()

    sorted_list = sorted(freq_dict.items(), key=operator.itemgetter(1))
    sorted_list.reverse()

    return sorted_list[:100]


def extract_frequent_words(mysql_query, is_repost=None):
    # connect MySQL
    config = {'host':***REMOVED***,
              'port':***REMOVED***,
              'user': ***REMOVED***,
              'password': ***REMOVED***,
              'database': ***REMOVED***}
    conn = msc.connect(**config)
    qry = conn.cursor(buffered=True)

    # twitter DB에 대해 최빈단어 분석
    qry.execute(mysql_query)
    result_qry = qry.fetchall()
    if is_repost == True:
        twitter_df = pd.DataFrame(data=result_qry,
                                  columns=['Twitter_ID', 'Screen_Name', 'Inclination', 'Date', 'URL', 'Contents',
                                           'Favorite', 'Retweet', 'Origin_ID', 'Origin_Screen_Name', 'Origin_URL'])
    else:
        twitter_df = pd.DataFrame(data=result_qry,
                                  columns=['Twitter_ID', 'Screen_Name', 'Inclination', 'Date', 'URL', 'Contents',
                                           'Favorite', 'Retweet'])

    # NLP Engines Predifine
    Kkma = 0
    Hannanum = 1
    Mecab = 2
    Twitter = 3

    nlp = NLP_Engine()
    word_list = list()
    for text in twitter_df['Contents']:
        result = nlp.ExtractPOS(text, Twitter)
        for word, pos in result:
            if pos in list(['Noun', 'Verb', 'Adjective', 'Adverb']):
                word_list.append(word)
            else:
                continue

    word_freq = Counter(word_list)

    return word_freq.most_common(100)

    # word_freq = {}
    # for text in twitter_df['Contents']:
    #     token = nlp.ExtractPOS(text, Kkma)
    #     for word in token:
    #         if word[1] in list(['NNG', 'NNP', 'VV', 'VA', 'MM', 'MAG']):
    #             if word[0] in word_freq:
    #                 word_freq[word[0]] = word_freq[word[0]] + 1
    #             else:
    #                 word_freq[word[0]] = 1
    #
    # sorted_list = sorted(word_freq.items(), key=operator.itemgetter(1))
    # sorted_list.reverse()
    #
    # for i in range(0, 20):
    #     print("Rank %2d. %s" % (i+1, sorted_list[i]))
    #
    # return sorted_list


if __name__ == '__main__':
    print("******** 보수 정치인 Top 20 words ********")
    query = "Select * from twitter_tweet where Inclination = 1"
    extract_frequent_words(query)
    print()

    print("***** 보수 정치인 리트윗 Top 20 words *****")
    query = "Select * from twitter_retweet where Inclination = 1"
    extract_frequent_words(query, is_repost=True)
    print()

    print("****** 보수 정치인 답글 Top 20 words ******")
    query = "Select * from twitter_reply where Inclination = 1"
    extract_frequent_words(query, is_repost=True)
    print()

    print("******** 진보 정치인 Top 20 words ********")
    query = "Select * from twitter_tweet where Inclination = 2"
    extract_frequent_words(query)
    print()

    print("***** 진보 정치인 리트윗 Top 20 words *****")
    query = "Select * from twitter_retweet where Inclination = 2"
    extract_frequent_words(query, is_repost=True)
    print()

    print("****** 진보 정치인 답글 Top 20 words ******")
    query = "Select * from twitter_reply where Inclination = 2"
    extract_frequent_words(query, is_repost=True)
    print()
