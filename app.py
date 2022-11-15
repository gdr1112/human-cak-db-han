# -*- coding: utf-8 -*-

from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text 
import pandas as pd 
import psycopg2
import time
import json
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

# 크롤링할 창 열기
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver.get("https://safecity.seoul.go.kr/acdnt/sbwyIndex.do")

# 크롤링 변수설정
parentElement = driver.find_elements(By.XPATH, '//*[@id="dv_as_timeline"]/li')

# 사고 정보 리스트
subli=[]

# 사고 정보 리스트에 크롤링해서 정보 넣기 (ul 태그 아래 있는 li 반복 뽑기)
for i in parentElement:
    i.click()
    time.sleep(0.05)
    a = i.text
    subli.append(a)
    i.click()

# 카톡으로 보내줄 문자열
sbstr=""

for item in subli:
    sbstr = sbstr + item + "\n"



app = Flask(__name__)

@app.route("/")
def index():
    return "hello"


## 크롤링
@app.route('/api/saysubway', methods=['POST'])
def saysubway():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

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



# ## DB 연결 Local
# def db_create():
#     # 로컬
# 	# engine = create_engine("postgresql://postgres:1234@localhost:5432/chatbot", echo = False)
		
# 	# # Heroku
#     # engine = create_engine("postgresql://avcdjxublgzxpt:208785dbb0dc2ae32038697ee3e56d141f070143b047110ac8886962cd59f969@ec2-52-1-17-228.compute-1.amazonaws.com:5432/d8i34lbtd4iht5", echo = False)

#     # engine.connect()

#     # postgre db 연결 - 개인설정 참고
#     conn = psycopg2.connect(host="ec2-52-1-17-228.compute-1.amazonaws.com", 
#                             dbname="d8i34lbtd4iht5", 
#                             user="avcdjxublgzxpt", 
#                             password="208785dbb0dc2ae32038697ee3e56d141f070143b047110ac8886962cd59f969", 
#                             port="5432")
    
#     # 데이터 조작 인스턴스 생성
#     cur = conn.cursor()

#     # 테이블 생성(create)
#     cur.execute("CREATE TABLE IF NOT EXISTS subdata(subacc VARCHAR(20) NOT NULL, acctime VARCHAR(30) NOT NULL, content VARCHAR(300) NOT NULL);")
#     conn.commit()


# 1단계 : 코드 수정
# 2단계 : 스킬 등록 (URL)
# 3단계 : 시나리오에서 등록한 스킬 호출
# 4단계 : 배포

## 카카오톡 텍스트형 응답
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