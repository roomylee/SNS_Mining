# -*- coding: utf-8 -*-
from flask import Flask, render_template
from sqlalchemy import create_engine
import pytagcloud
from NLP import *
import numpy as np

app = Flask(__name__)
***REMOVED***


query = "Select * from twitter_reply where Inclination=2"
words_left = extract_frequent_words(query, is_repost=True)

avg = np.mean(list(zip(*words_left))[1])
taglist = pytagcloud.make_tags(words_left[:100], maxsize=15*(words_left[0][1]-avg)/(avg-words_left[99][1]))
pytagcloud.create_tag_image(taglist, './static/img/wordcloud_left.jpg', size=(600, 400), fontname='BMHANNA_11yrs_ttf', rectangular=False)
print("Left done!")


query = "Select * from twitter_reply where Inclination=1"
words_right = extract_frequent_words(query, is_repost=True)

avg = np.mean(list(zip(*words_right))[1])
taglist = pytagcloud.make_tags(words_right[:100], maxsize=15*(words_right[0][1]-avg)/(avg-words_right[99][1]))
pytagcloud.create_tag_image(taglist, './static/img/wordcloud_right.jpg', size=(600, 400), fontname='BMHANNA_11yrs_ttf', rectangular=False)
print("Right done!")



@app.route('/')
def main():
    return render_template('integration.html', db_left=words_left, db_right=words_right)

@app.route('/politician')
def politician():
    return render_template('politician.html')

@app.route('/reply')
def reply():
    return render_template('reply.html')

@app.route('/aaaaa')
def ajaxtest():
    # url =/aaaaa?param1='문재인'&param2='

    return ;

if __name__ == '__main__':
    app.run()
