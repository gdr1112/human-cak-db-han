# -*- coding: utf-8 -*-

from flask import Flask, request
from datetime import date
import requests
import psycopg2
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "hello human"

## 오늘의 사고내역 보내주기
@app.route('/api/saysubway', methods=['POST'])
def saysubway():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    # db연결
    conn = psycopg2.connect(host="ec2-52-3-200-138.compute-1.amazonaws.com", 
                            dbname="d53l8l8j3pnlen", 
                            user="uholaamsnycauj", 
                            password="e0888df034f131c4de0a1d990150af4efef839fc4ed0ca087c6e489c586d098b", 
                            port="5432")

    # 데이터 조작 인스턴스 생성
    cur = conn.cursor()

    # 오늘 날짜 (YYYY-MM-DD 구하기)
    today = date.today().isoformat() + '%'

    # DB SELECT
    cur.execute(f"SELECT * FROM subaccdata WHERE acctime LIKE '{today}' order by acctime ASC")
    result_all = cur.fetchall()

    sbstr=""
    
    for i in result_all:
        for j in i:
            sbstr = sbstr + j + "\n"
        sbstr = sbstr + "\n"
    
    if(sbstr==""):
        sbstr = "오늘은 지하철 속보가 없습니다"
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": sbstr
                    }
                }
            ]
        }
    }
    return responseBody

# 경로 url 전달 함수
def location(searching):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
    headers = {
        "Authorization": "KakaoAK bbc0593ca1fbd88db71ccfdd5421ef1e"
    }
    destination = 'https://map.kakao.com/link/to/' + (requests.get(url, headers = headers).json()['documents'])[0].get('id')
    
    return destination

# 경로찾기 응답
@app.route('/api/goto', methods=['POST'])
def goto():
    body = request.get_json()
    print(body)
    params_df = (body['action']['params'])['sys_location']
    print(type(params_df))

    answer_text = str(location(params_df))

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text
                    }
                }
            ]
        }
    }

    return responseBody


# 1단계 : 코드 수정
# 2단계 : 스킬 등록 (URL)
# 3단계 : 시나리오에서 등록한 스킬 호출
# 4단계 : 배포

# 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody

## 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody

## 메인 로직!! 
def cals(opt_operator, number01, number02):
    if opt_operator == "addition":
        return number01 + number02
    elif opt_operator == "subtraction": 
        return number01 - number02
    elif opt_operator == "multiplication":
        return number01 * number02
    elif opt_operator == "division":
        return number01 / number02

## 카카오톡 Calculator 계산기 응답
@app.route('/api/calCulator', methods=['POST'])
def calCulator():
    body = request.get_json()
    print(body)
    params_df = body['action']['params']
    print(type(params_df))
    opt_operator = params_df['operators']
    number01 = json.loads(params_df['sys_number01'])['amount']
    number02 = json.loads(params_df['sys_number02'])['amount']

    print(opt_operator, type(opt_operator), number01, type(number01))

    answer_text = str(cals(opt_operator, number01, number02))

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text
                    }
                }
            ]
        }
    }

    return responseBody



# if __name__ == "__main__":
#     db_create()
#     app.run()