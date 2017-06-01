# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../../')

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
import json
import pytagcloud
from NLP import *
from word2vec.word2vec_module import *

app = Flask(__name__)
***REMOVED***

# 정치인 리스트 및 딕셔너리
politician_dic={
    "김부겸":"hopekbk", "김성식":"okkimss", "김진표":"jinpyokim",
    "문재인":"moonriver365", "민병두":"bdmin1958", "박범계":"bkfire1004",
    "박영선":"Park_Youngsun", "박원순":"wonsoonpark", "박지원":"jwp615",
    "송영길":"Bulloger", "안철수":"cheolsoo0919", "안희정":"steelroot",
    "이재명":"Jaemyung_Lee","정동영":"coreacdy","정세균":"sk0926",
    "진영":"Chinyoung0413", "천정배":"jb_1000", "추미애":"choomiae",
    "표창원":"DrPyo", "김경진":"2016kimkj", "주승용":"joo350",
    "안민석":"eduhimang", "이정미":"jinbo27", "박주민":"yoeman6310",
    "심상정":"sangjungsim", "김한길":"hangillo",
    "김무성":"kimmoosung","김진태":"jtkim1013","나경원":"Nakw",
    "남경필":"yesKP","서청원":"scw0403","심재철":"cleanshim",
    "원유철":"won6767","원희룡":"wonheeryong","이준석":"junseokandylee",
    "정우택":"bigwtc","정진석":"js0904",
    "최경환":"khwanchoi", "주호영":"sangtoil", "하태경":"taekyungh",
    "이완영":"yiwy57", "유승민":"yooseongmin2017", "황영철":"hhhyc",
    "김문수":"kimmoonsoo1", "이혜훈":"leehyehoon", "정병국":"withbg",
    "이종구":"lee_jongkoo"
}
left_politician = [
    "김부겸","김성식","김진표","문재인","민병두","박범계","박영선",
    "박원순","박지원","송영길","안철수","안희정","이재명","정동영",
    "정세균","진영","천정배","추미애","표창원", "김경진", "주승용",
    "안민석","이정미","박주민","심상정","김한길"
]
left_Screen_Name = [
    "hopekbk", "okkimss", "jinpyo_kim", "moonriver365",
    "bdmin1958", "bkfire1004", "Park_Youngsun", "wonsoonpark",
    "jwp615", "Bulloger", "cheolsoo0919", "steelroot",
    "Jaemyung_Lee","coreacdy","sk0926", "Chinyoung0413",
    "jb_1000", "choomiae", "DrPyo", "2016kimkj", "joo350",
    "eduhimang","jinbo27","yoeman6310","sangjungsim","hangillo"
]

right_politician = [
    "김무성","김진태","나경원","남경필","서청원","심재철","원유철",
    "원희룡","이준석","정우택","정진석","최경환","주호영",
    "하태경","이완영","유승민","황영철","김문수","이혜훈","정병국",
    "이종구"
]
right_Screen_Name = [
    "kimmoosung","jtkim1013","Nakw","yesKP","scw0403",
    "cleanshim","won6767","wonheeryong","junseokandylee",
    "bigwtc","js0904","khwanchoi","sangtoil","taekyungh",
    "yiwy57","yooseongmin2017","hhhyc","kimmoonsoo1","leehyehoon",
    "withbg","lee_jongkoo"
]
left_select = left_politician
right_select = right_politician


def make_Screen_Name_list(people_list):
    result_list = []
    for one in people_list:
        result_list.append(politician_dic[one])
    return result_list

def make_word_cloud(word_list, file_name):
    avg = np.mean(list(zip(*word_list))[1])
    taglist = pytagcloud.make_tags(word_list[:100],
                                   maxsize=20 * (word_list[0][1] - (avg) + 1) / (avg))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_%s.jpg' % file_name, size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("%s done!" % file_name)


def make_point_data(word_list, vec_list, inclinatation):
    point_data = '['
    for idx in range(len(vec_list)):
        if idx != 0:
            point_data += ","
        point_data += "{name:'%s',word:'%s',x:%s,y:%s,z:%s" \
                      % (inclinatation,word_list[idx][0], vec_list[idx][0][0], vec_list[idx][0][1], vec_list[idx][0][2])
        for rank in range(5):
            point_data += ",top%d:'%s'" % (rank, vec_list[idx][1][rank][0])
        point_data += '}'
    point_data += ']'

    return point_data

def extract_both_word(left_word, right_word):
    left_dic = {}
    both_word = []
    new_left_word = []
    new_right_word = []
    for l in left_word:
        left_dic[l[0]] = True

    for r in right_word:
        if r[0] in left_dic:
            left_dic[r[0]] = False
            both_word.append(r)
        else:
            new_right_word.append(r)

    for l in left_word:
        if left_dic[l[0]] is True:
            new_left_word.append(l)

    return new_left_word, new_right_word, both_word



# 메인 페이지 라우팅
@app.route('/')
def main():
    # 진보 진영의 워드클라우드 생성
    left_total_word = get_frequent_words(make_Screen_Name_list(left_select), ["left_frequency", "left_reply_frequency"])
    #make_word_cloud(word_list=left_word, file_name="left")

    # 보수 진영의 워드클라우드 생성
    right_total_word = get_frequent_words(make_Screen_Name_list(right_select), ["right_frequency", "right_reply_frequency"])
    #make_word_cloud(word_list=right_word, file_name="right")


    # 진보/보수 동시에 나타나는 차트 그리기위한 전처리
    left_word, right_word, both_word = extract_both_word(left_total_word, right_total_word)
    # 진보, 보수, 진보&보수, 3가지 class에 대한 vector 값 구하기
    left_vec = vectorize(left_word, "twitter_tweet", "twitter_reply")
    right_vec = vectorize(right_word, "twitter_tweet", "twitter_reply")
    both_vec = vectorize(both_word, "twitter_tweet", "twitter_reply")
    # 진보, 보수, 진보&보수, 3가지 class의 단어와 유사단어, vector를 합쳐 형식에 맞춰 생
    left_data = make_point_data(left_word, left_vec, "진보")
    right_data = make_point_data(right_word, right_vec, "보수")
    both_data = make_point_data(both_word, both_vec, "진보&보수")

    # 진보 차트 그리기
    left_only_vec = vectorize(left_total_word, "twitter_tweet", "twitter_reply")
    left_only_data = make_point_data(left_total_word, left_only_vec, "진보")

    # 보수 차트 그리기
    right_only_vec = vectorize(right_total_word, "twitter_tweet", "twitter_reply")
    right_only_data = make_point_data(right_total_word, right_only_vec, "보수")


    # 통합 버전 html 파일로 실행
    return render_template('integration.html',
                           left_freq=left_total_word, right_freq=right_total_word,
                           left_data=left_data, right_data=right_data, both_data=both_data,
                           left_only_data=left_only_data, right_only_data=right_only_data,
                           left_select=json.dumps(left_select),
                           right_select=json.dumps(right_select))















# 정치인 작성 트윗 라우팅
@app.route('/tweet')
def tweet():
    # 진보 진영 워드클라우드 생성
    left_word = get_frequent_words(make_Screen_Name_list(left_select), ["left_frequency"])
    avg = np.mean(list(zip(*left_word))[1])
    taglist = pytagcloud.make_tags(left_word[:100],
                                   maxsize=20 * (left_word[0][1] - (avg)+1) / (avg))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_left.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Left done!")

    # 보수 진영 워드클라우드 생성
    right_word = get_frequent_words(make_Screen_Name_list(right_select), ["right_frequency"])
    avg = np.mean(list(zip(*right_word))[1])
    taglist = pytagcloud.make_tags(right_word[:100],
                                   maxsize=20 * (right_word[0][1] - (avg)+1) / (avg))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_right.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Right done!")

    left_vec = vectorize(left_word)
    #left_vec = pca_projection(left_vec)
    right_vec = vectorize(right_word)
    #right_vec = pca_projection(right_vec)

    left_data = '['
    for idx in range(len(left_vec)):
        if idx != 0:
            left_data += ","
        left_data += "{name:'진보',word:'%s',x:%s,y:%s,z:%s}" \
                     % (left_word[idx][0], left_vec[idx][0], left_vec[idx][1], left_vec[idx][2])
    left_data += ']'

    right_data = '['
    for idx in range(len(right_vec)):
        if idx != 0:
            right_data += ","
        right_data += "{name:'보수',word:'%s',x:%s,y:%s,z:%s}" \
                      % (right_word[idx][0], right_vec[idx][0], right_vec[idx][1], right_vec[idx][2])
    right_data += ']'


    # 트윗에 대한 html 파일로 실행
    return render_template('tweet.html',
                           left_freq=left_word, right_freq=right_word,
                           left_data=left_data, right_data=right_data,
                           left_select=json.dumps(left_select),
                           right_select=json.dumps(right_select))

# 답글 라우팅
@app.route('/reply')
def reply():
    # 진보 워드클라우드
    left_word = get_frequent_words(make_Screen_Name_list(left_select), ["left_reply_frequency"])
    avg = np.mean(list(zip(*left_word))[1])
    taglist = pytagcloud.make_tags(left_word[:100],
                                   maxsize=20 * (left_word[0][1] - (avg)+1) / (avg))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_left.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Left done!")

    # 보수 워드클라우드
    right_word = get_frequent_words(make_Screen_Name_list(right_select), ["right_reply_frequency"])
    avg = np.mean(list(zip(*right_word))[1])
    taglist = pytagcloud.make_tags(right_word[:100],
                                   maxsize=20 * (right_word[0][1] - (avg)+1) / (avg))
    pytagcloud.create_tag_image(taglist, './static/img/wordcloud_right.jpg', size=(600, 400),
                                fontname='BMHANNA_11yrs_ttf', rectangular=False)
    print("Right done!")

    left_vec = vectorize(left_word)
    #left_vec = pca_projection(left_vec)
    right_vec = vectorize(right_word)
    #right_vec = pca_projection(right_vec)

    left_data = '['
    for idx in range(len(left_vec)):
        if idx != 0:
            left_data += ","
        left_data += "{name:'진보',word:'%s',x:%s,y:%s,z:%s}" \
                     % (left_word[idx][0], left_vec[idx][0], left_vec[idx][1], left_vec[idx][2])
    left_data += ']'

    right_data = '['
    for idx in range(len(right_vec)):
        if idx != 0:
            right_data += ","
        right_data += "{name:'보수',word:'%s',x:%s,y:%s,z:%s}" \
                      % (right_word[idx][0], right_vec[idx][0], right_vec[idx][1], right_vec[idx][2])
    right_data += ']'

    return render_template('reply.html',
                           left_freq=left_word, right_freq=right_word,
                           left_data=left_data, right_data=right_data,
                           left_select=json.dumps(left_select),
                           right_select=json.dumps(right_select))


# 체크박스에 대한 ajax처리, 선택한 정치인에 대한 정보 받아옴.
@app.route('/checkbox', methods=["GET", "POST"])
def check_box():
    if request.method == 'POST':
        global left_select, right_select
        left_select = request.json["left"]
        right_select = request.json["right"]
    return str(request.json);

# 실행
if __name__ == '__main__':
    app.run()
    #app.run(host="166.104.140.76", port=50000)
