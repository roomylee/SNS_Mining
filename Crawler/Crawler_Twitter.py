# My ID : 553557460
import tweepy
import mysql.connector as msc
import mysql.connector.errors
import pandas as pd
from datetime import datetime, timedelta
import time

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

# 매개변수 id를 user_id로 갖는 인물의
# Tweet을 수집하여 twitter_tweet DB에 저장
def collect_tweet(id, inclination):
    # tweepy.Cursor를 통해서 타임라인 게시글 탐색
    cursor = tweepy.Cursor(api.user_timeline, user_id=id).items()

    while True:
        try:
            post = cursor.next()

            # API user_timeline() attribute 설명
            # screen_name : @닉네임
            # created_at : 게시글 생성 시간
            # id : 게시글 ID(URL)
            # text : 게시글 내용
            # favorite_count : 좋아요 개수
            # retweet_count : 리트윗 개수
            screen_name = post.author.screen_name
            date = post.created_at + timedelta(hours=9) # 한국시간으로 변환(+9시간)
            url = post.id
            content = post.text
            favorite = post.favorite_count
            retweet = post.retweet_count

            content = content.replace("'","\\\'")

            # INSERT Query 생성
            insert_qry = "INSERT IGNORE INTO twitter_tweet VALUES('%s', '%s', %d, '%s', '%s', '%s', %d, %d)" \
                        % (id, screen_name, inclination, date, url, content, favorite, retweet)

            # INSERT Query 실행
            qry.execute(insert_qry)
            conn.commit()

        # Tweepy API Interval
        except tweepy.TweepError:
            print("Waits...")
            time.sleep(60 * 15 + 1)
            print("Wake up!")
            continue

        except mysql.connector.errors.ProgrammingError:
            print("MySQL Programming ERROR")
            print("Query: %s" % insert_qry)
            continue

        except StopIteration:
            break

# 매개변수의 query는 검색하고자 하는 유저의 @Screen_Name
# 해당 유저의 게시글에 대해 retweet(리트윗) 또는 reply(답글)하고 있는 Tweet을 수집하여
# twitter_retweet 또는 twitter_reply DB에 저장
def collect_repost(query, inclination):
    # tweepy.Cursor를 통해서 타임라인 게시글 탐색
    cursor = tweepy.Cursor(api.search, q=query).items(1000)

    while True:
        try:
            post = cursor.next()

            # API user_timeline() attribute 설명
            # screen_name : @닉네임
            # created_at : 게시글 생성 시간
            # id : 게시글 ID(URL)
            # text : 게시글 내용
            # favorite_count : 좋아요 개수
            # retweet_count : 리트윗 개수
            screen_name = post.author.screen_name
            date = post.created_at + timedelta(hours=9)  # 한국시간으로 변환(+9시간)
            url = post.id
            content = post.text
            favorite = post.favorite_count
            retweet = post.retweet_count

            content = content.replace("'", "\\\'")

            if hasattr(post, 'retweeted_status'):
                # origin : 원본에 대한 정보
                origin_id = post.author.id
                origin_screen_name = post.retweeted_status.user.screen_name
                origin_url = post.retweeted_status.id

                if "@%s" % origin_screen_name != query:
                    continue

                # INSERT Query 생성
                insert_qry = "INSERT IGNORE INTO twitter_retweet VALUES('%s', '%s', %d, '%s', '%s', '%s', %d, %d, '%s', '%s', '%s')" \
                             % (id, screen_name, inclination, date, url, content, favorite, retweet, origin_id, origin_screen_name, origin_url)
            else:
                # origin : 원본에 대한 정보
                origin_id = post.in_reply_to_user_id
                origin_screen_name = post.in_reply_to_screen_name
                origin_url = post.in_reply_to_status_id

                if "@%s" % origin_screen_name != query:
                     continue

                # INSERT Query 생성
                insert_qry = "INSERT IGNORE INTO twitter_reply VALUES('%s', '%s', %d, '%s', '%s', '%s', %d, %d, '%s', '%s', '%s')" \
                             % (id, screen_name, inclination, date, url, content, favorite, retweet, origin_id, origin_screen_name, origin_url)

            # INSERT Query 실행
            qry.execute(insert_qry)
            conn.commit()

        # Tweepy API Interval
        except tweepy.TweepError:
            print("Waits...")
            time.sleep(60 * 15 + 1)
            print("Wake up!")
            continue

        except mysql.connector.errors.ProgrammingError:
            print("MySQL Programming ERROR")
            print("Query: %s" % insert_qry)
            continue

        except StopIteration:
            break

if __name__ == '__main__':
    # 타켓 정치인 목록 가져오기
    qry.execute("SELECT * FROM politician")
    politician = qry.fetchall()
    user_list = pd.DataFrame(data=politician, columns=['Name', 'Screen_Name', 'Twitter_ID', 'Inclination'])

    flag = False
    for index, row in user_list.iterrows():
        name = row['Name']
        screen_name = row['Screen_Name']
        id = row['Twitter_ID']
        inclination = row['Inclination']

        # if name == "김진표":
        #     flag = True
        # if flag != True:
        #     continue

        print("Crawling %s's tweet..." % name)
        collect_tweet(id, inclination)
        print("Complete Crawling %s's tweet!" % name)

        print("Crawling Repost(Retweet/Reply) to %s's tweet" % name)
        collect_repost("@%s" % screen_name, inclination)
        print("Complete Crawling Repost(Retweet/Reply) to %s's tweet" % name)


qry.close()
conn.close()
