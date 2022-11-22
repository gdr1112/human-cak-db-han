import psycopg2
import os
import sys
import requests
import datetime
import time
import re
import schedule

# html 디코딩 함수
def clean_html(x):
  x = re.sub("\&\w*\;","",x)
  x = re.sub("<.*?>","",x)
  return x



def insertnews():
    now = time

    print(print("time log :", now.strftime('%Y-%m-%d %H:%M:%S')))
    # db연결
    conn = psycopg2.connect(host="ec2-23-21-207-93.compute-1.amazonaws.com", 
                            dbname="d3oubpekvnbupv", 
                            user="grxhirqndvyqvv", 
                            password="6f1afaafe16d245c70666bdb8c831aa876e62b380a1544f5dc832c51f27cece6", 
                            port="5432")

    # 데이터 조작 객체 생성
    cur = conn.cursor()

    # 네이버 검색api 키값
    client_id = 'CmmN2OJp47c60h9IWTRs'
    client_secret = 'mALduPDQEB'

    #검색설정
    search_word = '지하철 사고'
    encode_type = 'json'
    max_display = 50
    sort = 'date'
    start = 1

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"

    #헤더에 아이디와 키 정보 넣기
    headers = {'X-Naver-Client-Id' : client_id,
            'X-Naver-Client-Secret':client_secret
            }

    #HTTP요청 보내기
    r = requests.get(url, headers=headers)
    #요청 결과 보기 200 이면 정상적으로 요청 완료
    print(r)
    # json형식으로 받기
    result = r.json()

    # key : items
    result_items=result['items']

    # db에 저장하기

    for i in result_items:
        
        # 날짜 형식 변환
        pDate = datetime.datetime.strptime(i['pubDate'][5:-6], '%d %b %Y %H:%M:%S')
        pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
        
        # 뉴스제목 디코딩
        title = clean_html(i['title'])
        
        link = i['link']
        
        insertdata = (pDate, title, link)
        
        # ON CONFLICT : 데이터가 중복되면 INSERT하지않음
        cur.execute("INSERT into newsdata(newsdate, newsname, newslink) VALUES (%s, %s, %s) ON CONFLICT (newsname, newslink) DO NOTHING", insertdata)

    # db commit
    conn.commit()   

def exit():
    sys.exit()

schedule.every(10).minutes.do(insertnews)
schedule.every().day.at("23:55").do(exit)

while True:
    schedule.run_pending()
    time.sleep(1)