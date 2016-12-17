# My ID : 553557460
import tweepy
import mysql.connector as msc
import pandas as pd
from datetime import datetime, timedelta

# Twitter Developer Account Info.
API_KEY = ***REMOVED***
API_SECRET = ***REMOVED***
ACCESS_KEY = ***REMOVED***
ACCESS_SECRET = ***REMOVED***

oAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oAuth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth_handler=oAuth)

# Database Account Info.
config = {'user':***REMOVED***,
        'password':***REMOVED***,
        'database':***REMOVED***}
conn = msc.connect(**config)
qry = conn.cursor(buffered=True)

if __name__ == '__main__':
    # 타켓 정치인 목록 가져오기
    qry.execute("SELECT * FROM politician")
    politician = qry.fetchall()
    user_list = pd.DataFrame(data=politician, columns=['Name', 'Twitter_ID', 'Inclination'])

    for index, row in user_list.iterrows():
        id = row['Twitter_ID']
        print("Crawling %s's twitter..." % row['Name'])

        # 해당 인물의 가장 최근 게시글 검색 -> 새로 올린 글만 DB에 INSERT 하기 위해
        qry.execute("SELECT MAX(Date) FROM twitter WHERE Twitter_ID = %s" % id)
        recent_date = qry.fetchall()[0][0]

        # tweepy.Cursor를 통해서 타임라인 게시글 탐색   
        for post in tweepy.Cursor(api.user_timeline, user_id=id).items():
            # API user_timeline() attribute 설명
            # screen_name : 닉네임
            # created_at : 게시글 생성 시간
            # id : 게시글 ID(URL)
            # text : 게시글 내용
            # favorite_count : 좋아요 개수
            # retweet_count : 리트윗 개수
            nickname = post.author.screen_name
            date = post.created_at + timedelta(hours=9) # 한국시간으로 변환(+9시간)
            url = post.id
            content = post.text
            favorite = post.favorite_count
            retweet = post.retweet_count

            # INSERT Query 생성
            insert_qry = "INSERT INTO twitter VALUES('%s', '%s', '%s', '%s', '%s', %d, %d)" \
                        % (id, nickname, date, url, content, favorite, retweet)
            # DB에 없는 최신 게시글만 INSERT
            if recent_date != None and recent_date >= date:
                break

            # INSERT Query 실행
            try:
                qry.execute(insert_qry)
                conn.commit()
            except:
                conn.rollback()

            print("Complete Crawling %s's twitter!" % row['Name'])

qry.close()
conn.close()
