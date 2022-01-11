#-*- coding:utf-8 -*- 

# settings : change directory, import modules
import pymysql
import yfinance as yf
import json
import matplotlib.pyplot as plt
import datetime
from tqdm.notebook import tqdm
import pandas as pd
import os
# dropbox로 이동
change_path = "C:/Users/enkee/Dropbox/SNURO_LA/[100]Data/Zoom_Clova"
os.chdir(change_path)
changed = os.getcwd()
print(changed)

pd.set_option('display.max_rows', None)

# function 1. 이번주의 dropbox file list
def get_files(week):
    file_list = [file for file in os.listdir('./') if file.startswith(f'{week}주차_') and file.endswith('.txt')]
    print("file_list: {}".format(file_list))
    return file_list

# function 1. 이번주의 dropbox file list
def missingTeam(fileList):
    xlsx = pd.read_excel('./스누로_3기_matching.xlsx')
    print(xlsx.head(10)) # col : 스누링커 스누씨드
    mentor_list = xlsx.groupby(['스누링커']).count()
    mentor_list['스누링커'] = mentor_list.index
    mentor_list = mentor_list['스누링커'].values.tolist()
    
    missingMentor = []
    fileList = [file[4:-4] for file in fileList]
    
    for i in range(len(mentor_list)):
        if mentor_list[i] not in fileList:
            missingMentor.append(mentor_list[i])

    print(f"멘토 수 : {len(mentor_list)}")
    print(f"파일 수 : {len(fileList)}")
    
    if len(missingMentor) == 0:
        print("모든 멘토가 파일을 제출하였습니다 :)")
    else:
        print("\n제출하지 않았거나 파일 양식 오류가 발생한 멘토 목록입니다 : \n", missingMentor)
    
    return len(mentor_list)

# function 1. 데이터 전처리 (from txt to df)
def preprocessing(fileName):
    df = pd.DataFrame(index = range(0,4),columns=['participants', 'time', 'sentence'])
    file = open(f'{fileName}', 'r', encoding = 'utf-8')
    
    tmp = 0
    tmp_line = []
    
    while True:
        line = file.readline()
        if line[:1] == "멘":
            if tmp != 0:
                df.loc[f'{tmp}'] = tmp_line[:3]
                if len(tmp_line) > 3:
                    # 길어진 문장에 대해서도 처리해주기 :)
                    pass
            tmp_line = []
            tmp += 1
            tmp_line.append(line[:-6])
            tmp_line.append(line[-5:-1])
        elif line == '\n':
            pass
        else:
            tmp_line.append(line[:-1])
        if not line: break
    # drop na value
    df = df.dropna(axis=0)
    return df

# function 1. send df to DB
def database(fileName, weekNum, df):
    # step 0. Connect to DB server
    ip = '192.168.35.161'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()
    
    # step 1. Create DB
    database = 'ZOOM'
    query = 'USE ZOOM'
    
    # database가 있으면, 갖다 쓰고
    try: curs.execute(query)
    except: 
    # 없으면 생성한다. 
        query = 'CREATE DATABASE ZOOM'
        curs.execute(query)
        query = 'USE ZOOM'
        curs.execute(query)

    # Check databases
    query = 'SHOW DATABASES'
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)
                
    # step 2. week Table 생성
    
    # Create Table
    fileName = fileName[:-4]
    tbName = f'{fileName}'
    try: 
        #  있으면 갖다 쓰고, 
        query = 'SELECT * FROM %s' % tbName
        curs.execute(query)
        result = curs.fetchall()
        for r in result:
            print(r)    
    except:
        # 없으면 CREATE
        query = '''
        CREATE TABLE %s (
            actor varchar(10),
            time char(10),
            sentence TEXT
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
        
    # step 3. Table에 df 삽입
    # Insert Data
    query_base = "INSERT INTO %s (actor, time, sentence)" % (tbName) +  "VALUES ('%s', '%s', '%s')"
    for i in tqdm(range(len(df))):
        actor = df.iloc[i]['participants']
        time = df.iloc[i]['time']
        sentence = df.iloc[i]['sentence']
        query = query_base % (actor, time, sentence)
        curs.execute(query)
    conn.commit()

    # Get data from Table
    query = 'SELECT * FROM %s' % tbName
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)
        print("HI")
        
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

    # curs.execute('DROP TABLE IF EXISTS AAPL')
    # check

# test
try:
    fileList = get_files(1)
    print(missingTeam(fileList[:-3]))
    for i in fileList:
        df = preprocessing(i)
        print(df.head(5))
        database(i, 1, df)
    
except:
    print("ERROR")

"""

# 안 낸 사람 체크

# step 1. get data

# step 2. db - make n week table

# step 3. insert data

# error handling

# DB에 보내기

def basic_preprocessing(textFile, participant_list):
    # open textFile
    df_to_save = pd.DataFrame(index = range(0,4),columns=['participants', 'time', 'sentence'])
    f = open(f'{textFile}', 'r', encoding='utf-8')
    # preprocessing
    tmp = 0
    tmp_line = []
    while True:
        line = f.readline()
        if line[:len(participant_list[1])] in participant_list:
            if tmp != 0:
                
                df_to_save.loc[f'{tmp}'] = tmp_line[:3]
            tmp_line = []
            tmp += 1
            tmp_line.append(line[:len(participant_list[1])])
            tmp_line.append(line[len(participant_list[1]):-1])
        elif line == '\n':
            pass
        else:
            tmp_line.append(line[:-1])
        if not line: break
    # drop na value
    df_to_save = df_to_save.dropna(axis=0)
    return df_to_save
        
for i in file_list:
    part = i[:-4].split(' ')
    f = open(i, 'r', encoding='utf-8')
    df = basic_preprocessing(i, part)
    print(df.head(20))
    f.close()


# table 만들기

# participants

# time

    
###########################
# Insert Data
query_base = "INSERT INTO %s (actor, time, sentence)" % (tbName) +  "VALUES ('%s', '%s', '%s')"
for i in tqdm(range(len(df))):
    actor = df.iloc[i]['participants']
    time = df.iloc[i]['time']
    sentence = df.iloc[i]['sentence']
    query = query_base % (actor, time, sentence)
    curs.execute(query)
conn.commit()

# Get data from Table
query = 'SELECT * FROM %s' % tbName
curs.execute(query)
result = curs.fetchall()
for r in result:
    print(r)
    print("HI")
    
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

# curs.execute('DROP TABLE IF EXISTS AAPL')

"""