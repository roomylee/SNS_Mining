import mysql.connector as msc
import pandas as pd
import operator
from NLP import NLP_Engine

# NLP Engines Predifine
Kkma = 0
Hannanum = 1
Mecab = 2
Twitter = 3

if __name__ == '__main__':

    # connect MySQL
    config = {'user':***REMOVED***,
            'password':***REMOVED***,
            'database':***REMOVED***}
    conn = msc.connect(**config)
    qry = conn.cursor(buffered=True)

    # twitter DB에 대해 최빈단어 분석 
    qry.execute("SELECT * FROM twitter_tweet")
    result_qry  = qry.fetchall()
    twitter_df = pd.DataFrame(data=result_qry, 
            columns=['Twitter_ID', 'Screen_Name', 'Date', 'URL', 'Contents', 'Favorite', 'Retweet'])
    
    nlp = NLP_Engine()
    word_freq = {}
    for text in twitter_df['Contents']:
        token = nlp.ExtractPOS(text, Mecab)
        for word in token:
            if word[1] in list(['NNG', 'NNP', 'VV', 'VA', 'MM', 'MAG']):
                if word[0] in word_freq:
                    word_freq[word[0]] = word_freq[word[0]] + 1
                else:
                    word_freq[word[0]] = 1

    sorted_list = sorted(word_freq.items(), key=operator.itemgetter(1))
    sorted_list.reverse()

    for i in range(0, 20):
        print(sorted_list[i])

