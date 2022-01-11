# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 00:33:40 2021

@author: User
"""
import pymysql
import pandas as pd
import yfinance as yf
import json
import matplotlib.pyplot as plt
import datetime
import time
from tqdm.notebook import tqdm

# function 0. menti / mentor data

# UNKIZ 아이디와 실명의 대응 여부

# 멘토별로 df 분리

# 주차별로 df 분리

def mentitor():
    xlsx = pd.read_excel('./pipeline/unkiz/스누로_3기_matching.xlsx')
    print(xlsx.head(10)) # col : 스누링커 스누씨드
    return xlsx

# function 1. load file and preprocessing
# start : '2021-12-14' end : '2021-12-15'
def preprocessing(start, end):
    
    # 기간 제한 기능 추가하기
    
    with open("./pipeline/unkiz/XAPI.json", "r", encoding="utf8") as f:
        contents = f.read() #String type
        json_data = json.loads(contents)
    
    #actor에서 name만 추출
    actor_list = []
    #object에서 definition - name - ko-KR에 있는 데이터만 담기
    object_list = []
    #verb에서 display - ko-KR만 추출
    verb_list = []
    #timestamp
    timestamp_list = []

    for i, xapi in enumerate(json_data):
        
        #object에 있는 결측치를 대체함
        if xapi['object'] == {}:
            json_data[i]['object'] = {'definition': {'name': {'ko-KR': 'none'}}}
        
        actor_var = xapi['actor']['name']
        object_var = xapi['object']['definition']['name']['ko-KR']
        verb_var = xapi['verb']['display']['ko-KR']
        timestamp_var = xapi['timestamp']

        actor_list.append(actor_var)
        object_list.append(object_var)
        verb_list.append(verb_var)
        timestamp_list.append(timestamp_var)

    df_data = pd.DataFrame(
        {
            'actor' : actor_list,
            'object' : object_list,
            'verb' : verb_list,
            'timestamp' : timestamp_list
        }
    )

    selectTime = df_data
    selectTime['timestamp'] = pd.to_datetime(selectTime['timestamp'], errors='ignore')

    selectTime = selectTime[selectTime['timestamp'] >= start]
    selectTime = selectTime[selectTime['timestamp'] < end]
    
    return selectTime

def tempDummy():
    xlsx = mentitor()
    df = preprocessing()
    print(xlsx)
    print(df)
    # UNKIZ 아이디와 실명의 대응 여부

    # 멘토별로 df 분리

    # 주차별로 df 분리
    


# function 3. connect to DB
def connectDB(df_data, week):
    # Connect to DB 192.168.35.161
    # https://xn--220b31d95hq8o.xn--3e0b707e/
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

    # Create DB
    database = 'UNKIZ'
    query = 'USE UNKIZ'
    try: curs.execute(query) # 이미 stock 존재
    except: 
        query = f'CREATE DATABASE {database}' # 생성
        curs.execute(query)
        query = f'USE {database}'
        curs.execute(query)

    # Check databases
    query = 'SHOW DATABASES'
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)

    # Create Table
    tbName = f'{week}주차'
    try: 
        query = 'SELECT * FROM %s' % tbName
        curs.execute(query)
        result = curs.fetchall()
        for r in result:
            print(r)    
    except:
        query = '''
        CREATE TABLE %s (
            actor varchar(10),
            object TEXT,
            verb char(10),
            time TIMESTAMP
            );
        ''' % tbName
        
        curs.execute(query)
        result = curs.fetchall()
        for r in result:
            print(r)    


    # Check Tables
    sql = 'SHOW TABLES'
    curs.execute(sql)
    result = curs.fetchall()
    for r in result:
        print(r)
        
    # 테이블 스키마 열람
    query = 'DESC %s' % list(result[0].values())[0]
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)
        
    # Insert Data
    query_base = "INSERT INTO %s (actor, object, verb, time)" % (tbName) +  "VALUES ('%s', '%s', '%s', '%s')"
    for i in tqdm(range(len(df_data))):
        print("HI")
        actor = df_data.iloc[i]['actor']
        object = df_data.iloc[i]['object']
        verb = df_data.iloc[i]['verb']
        time = df_data.iloc[i]['timestamp']
        query = query_base % (actor, object, verb, time)
        curs.execute(query)
    conn.commit()

    # Get data from Table
    query = 'SELECT * FROM %s' % tbName
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)
        
    # Get users
    query = 'USE mysql'
    curs.execute(query)
    query = 'SELECT user, host from USER'
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)

    conn.commit() 
    conn.close()


def makeDummy():
    participant = mentitor()
    participant = participant['스누씨드']
    participant = participant.tolist()


    # start : '2021-12-14' end : '2021-12-15'
    df = preprocessing('2021-12-14','2021-12-20') # 이상 미만 관계


    idList = df.loc[:, ['actor']]
    idList = idList.groupby('actor').count()
    idList = idList.index.tolist()
    print(idList)
    print(len(idList))

    # id test를 위한 dummy data 생성
    dummy = df
    for i in range(len(idList)):
        l = idList[i]
        r = participant[i]
        dummy.loc[dummy['actor']==l, 'actor'] = r
                            
    print(dummy.head(10))
    
    return dummy

connectDB(makeDummy(), 1)