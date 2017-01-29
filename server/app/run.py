# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
import json
import pytagcloud
from NLP import *
import numpy as np

app = Flask(__name__)
***REMOVED***


politician_dic={"김부겸":"hopekbk", "김성식":"okkimss", "김진표":"jinpyo_kim",
          "문재인":"moonriver365", "민병두":"bdmin1958", "박범계":"bkfire1004",
          "박영선":"Park_Youngsun", "박원순":"wonsoonpark", "박지원":"jwp615",
          "송영길":"Bulloger", "안철수":"cheolsoo0919", "안희정":"steelroot",
          "이재명":"Jaemyung_Lee","정동영":"coreacdy","정세균":"sk0926",
          "진영":"Chinyoung0413", "천정배":"jb_1000", "추미애":"choomiae",
          "표창원":"DrPyo",
          "김무성":"kimmoosung","김진태":"jtkim1013","나경원":"Nakw",
          "남경필":"yesKP","서청원":"scw0403","심재철":"cleanshim",
          "원유철":"won6767","원희룡":"wonheeryong","이준석":"junseokandylee",
          "장제원":"Changjewon","정우택":"bigwtc","정진석":"js0904",
          "최경환":"khwanchoi"}

left_politician = ["김부겸","김성식","김진표","문재인","민병두","박범계","박영선",
                "박원순","박지원","송영길","안철수","안희정","이재명","정동영",
                "정세균","진영","천정배","추미애","표창원"]
left_Screen_Name = ["hopekbk", "okkimss", "jinpyo_kim", "moonriver365",
                    "bdmin1958", "bkfire1004", "Park_Youngsun", "wonsoonpark",
                    "jwp615", "Bulloger", "cheolsoo0919", "steelroot",
                    "Jaemyung_Lee","coreacdy","sk0926", "Chinyoung0413",
                    "jb_1000", "choomiae", "DrPyo"]

right_politician = ["김무성","김진태","나경원","남경필","서청원","심재철","원유철",
                 "원희룡","이준석","장제원","정우택","정진석","최경환"]
right_Screen_Name = ["kimmoosung","jtkim1013","Nakw","yesKP","scw0403",
                    "cleanshim","won6767","wonheeryong","junseokandylee",
                    "Changjewon","bigwtc","js0904","khwanchoi"]

left_select = left_politician
right_select = right_politician

def make_Screen_Name_list(people_list):
    result_list = []
    for one in people_list:
        result_list.append(politician_dic[one])
    return result_list

@app.route('/')
def main():
    left_word = get_frequent_words(make_Screen_Name_list(left_select), ["left_frequency", "left_reply_frequency"])
    avg = np.mean(list(zip(*left_word))[1])
    taglist = pytagcloud.make_tags(left_word[:100],
                                   maxsize=12 * (left_word[0][1] - avg) / (avg - left_word[99][1]))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_left.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Left done!")

    right_word = get_frequent_words(make_Screen_Name_list(right_select), ["right_frequency", "right_reply_frequency"])
    avg = np.mean(list(zip(*right_word))[1])
    taglist = pytagcloud.make_tags(right_word[:100],
                                   maxsize=12 * (right_word[0][1] - avg) / (avg - right_word[99][1]))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_right.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Right done!")

    return render_template('integration.html',
                           left_freq=left_word, right_freq=right_word,
                           left_select=json.dumps(left_select),
                           right_select=json.dumps(right_select))

@app.route('/tweet')
def tweet():
    left_word = get_frequent_words(make_Screen_Name_list(left_select), ["left_frequency"])
    avg = np.mean(list(zip(*left_word))[1])
    taglist = pytagcloud.make_tags(left_word[:100],
                                   maxsize=12 * (left_word[0][1] - avg) / (avg - left_word[99][1]))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_left.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Left done!")

    right_word = get_frequent_words(make_Screen_Name_list(right_select), ["right_frequency"])
    avg = np.mean(list(zip(*right_word))[1])
    taglist = pytagcloud.make_tags(right_word[:100],
                                   maxsize=12 * (right_word[0][1] - avg) / (avg - right_word[99][1]))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_right.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Right done!")

    return render_template('integration.html',
                           left_freq=left_word, right_freq=right_word,
                           left_select=json.dumps(left_select),
                           right_select=json.dumps(right_select))

@app.route('/reply')
def reply():
    left_word = get_frequent_words(make_Screen_Name_list(left_select), ["left_reply_frequency"])
    avg = np.mean(list(zip(*left_word))[1])
    taglist = pytagcloud.make_tags(left_word[:100],
                                   maxsize=12 * (left_word[0][1] - avg) / (avg - left_word[99][1]))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_left.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Left done!")

    right_word = get_frequent_words(make_Screen_Name_list(right_select), ["right_reply_frequency"])
    avg = np.mean(list(zip(*right_word))[1])
    taglist = pytagcloud.make_tags(right_word[:100],
                                   maxsize=12 * (right_word[0][1] - avg) / (avg - right_word[99][1]))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_right.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Right done!")

    return render_template('integration.html',
                           left_freq=left_word, right_freq=right_word,
                           left_select=json.dumps(left_select),
                           right_select=json.dumps(right_select))


@app.route('/checkbox', methods=["GET", "POST"])
def check_box():
    if request.method == 'POST':
        global left_select, right_select
        left_select = request.json["left"]
        right_select = request.json["right"]
    return str(request.json);

if __name__ == '__main__':
    app.run()
