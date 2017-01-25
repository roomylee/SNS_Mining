# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
import json
import pytagcloud
from NLP import *
import numpy as np

app = Flask(__name__)
***REMOVED***


# query = "Select * from twitter_reply where Inclination=2"
# words_left = extract_frequent_words(query, is_repost=True)
#
# avg = np.mean(list(zip(*words_left))[1])
# taglist = pytagcloud.make_tags(words_left[:100], maxsize=13*(words_left[0][1]-avg)/(avg-words_left[99][1]))
# pytagcloud.create_tag_image(taglist, './static/img/wordcloud_left.jpg', size=(600, 400), fontname='BMHANNA_11yrs_ttf', rectangular=False)
# print("Left done!")
#
#
# query = "Select * from twitter_reply where Inclination=1"
# words_right = extract_frequent_words(query, is_repost=True)
#
# avg = np.mean(list(zip(*words_right))[1])
# taglist = pytagcloud.make_tags(words_right[:100], maxsize=13*(words_right[0][1]-avg)/(avg-words_right[99][1]))
# pytagcloud.create_tag_image(taglist, './static/img/wordcloud_right.jpg', size=(600, 400), fontname='BMHANNA_11yrs_ttf', rectangular=False)
# print("Right done!")

left_people = [["김부겸","김성식","김진표","문재인","민병두","박범계","박영선",
                "박원순","박지원","송영길","안철수","안희정","이재명","정동영",
                "정세균","진영","천정배","추미애","표창원"],
               ["hopekbk","okkimss","jinpyo_kim","moonriver365","bdmin1958",
                "bkfire1004","Park_Youngsun","wonsoonpark","jwp615","Bulloger",
                "cheolsoo0919","steelroot","Jaemyung_Lee","coreacdy","sk0926",
                "Chinyoung0413","jb_1000","choomiae","DrPyo",]]

right_people = [["김무성","김진태","나경원","남경필","서청원","심재철","원유철",
                 "원희룡","이준석","장제원","정우택","정진석","최경환",],
                ["kimmoosung","jtkim1013","Nakw","yesKP","scw0403","cleanshim",
                 "won6767","wonheeryong","junseokandylee","Changjewon","bigwtc",
                 "js0904","khwanchoi",]]


@app.route('/')
def main():
    with open('./static/json/init_left.json', 'r') as fp:
        left_word = json.load(fp=fp)
    with open('./static/json/init_right.json', 'r') as fp:
        right_word = json.load(fp=fp)

    return render_template('integration.html', db_left=left_word, db_right=right_word)

@app.route('/politician')
def politician():
    with open('./static/json/init_left_politician.json', 'r') as fp:
        left_word = json.load(fp=fp)
    with open('./static/json/init_right_politician.json', 'r') as fp:
        right_word = json.load(fp=fp)

    return render_template('politician.html', db_left=left_word, db_right=right_word)

@app.route('/reply')
def reply():
    with open('./static/json/init_left_reply.json', 'r') as fp:
        left_word = json.load(fp=fp)
    with open('./static/json/init_right_reply.json', 'r') as fp:
        right_word = json.load(fp=fp)

    return render_template('reply.html', db_left=left_word, db_right=right_word)


@app.route('/plist', methods=["GET", "POST"])
def politician_list():
    dict = {'left':left_people,
            'right':right_people}
    return json.dumps(dict, ensure_ascii=False)

@app.route('/check_box', methods=["GET", "POST"])
# url =/aaaaa?param1='문재인'&param2='
def check_box():
    if request.method == 'POST':
        left_word = get_frequent_words(left_people, ["left_reply_frequency"])
        with open('./static/json/result.json', 'w') as fp:
            json.dumps(obj=left_word, fp=fp)


    return ;

if __name__ == '__main__':


    # left_word = get_frequent_words(left_people[1], ["left_frequency", "left_reply_frequency"])
    # right_word = get_frequent_words(right_people[1], ["right_frequency", "right_reply_frequency"])
    # with open('./static/json/init_left.json', 'w') as fp:
    #     json.dump(obj=left_word, fp=fp)
    # with open('./static/json/init_right.json', 'w') as fp:
    #     json.dump(obj=right_word, fp=fp)
    #
    # left_word = get_frequent_words(left_people[1], ["left_frequency"])
    # right_word = get_frequent_words(right_people[1], ["right_frequency"])
    # with open('./static/json/init_left_politician.json', 'w') as fp:
    #     json.dump(obj=left_word, fp=fp)
    # with open('./static/json/init_right_politician.json', 'w') as fp:
    #     json.dump(obj=right_word, fp=fp)
    #
    # left_word = get_frequent_words(left_people[1], ["left_reply_frequency"])
    # right_word = get_frequent_words(right_people[1], ["right_reply_frequency"])
    # with open('./static/json/init_left_reply.json', 'w') as fp:
    #     json.dump(obj=left_word, fp=fp)
    # with open('./static/json/init_right_reply.json', 'w') as fp:
    #     json.dump(obj=right_word, fp=fp)



    app.run()
