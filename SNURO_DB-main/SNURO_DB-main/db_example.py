# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 00:33:40 2021

@author: User
"""
import pymysql
import pandas as pd
import yfinance as yf
import datetime
from tqdm.notebook import tqdm

# Get stock data
stock_name = 'AAPL'
start = '2019-01-01'
end = datetime.date.today().isoformat()

stock_data = yf.download(stock_name, start, end)

ticker = yf.Ticker('AAPL')
div = ticker.dividends[start:end]
split = ticker.splits[start:end]
analysis = ticker.recommendations[start:end]

# Connect to DB
ip = '211.212.8.227'
conn = pymysql.connect(host=ip, port=3306, user='lkm', password='lkm',
                       db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
curs = conn.cursor()

# Create DB
database = 'stock'
query = 'USE STOCK'
try: curs.execute(query)
except: 
    query = 'CREATE DATABASE stock'
    curs.execute(query)
    query = 'USE stock'
    curs.execute(query)
# Check databases
query = 'SHOW DATABASES'
curs.execute(query)
result = curs.fetchall()
for r in result:
    print(r)

# Create Table
try: 
    query = 'SELECT * FROM %s' % stock_name
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)    
except:
    query = '''
    CREATE TABLE %s (
        Date DATE,
        Open float,
        High float,
        Low float,
        Close float,
        Volume INT
        )
    ''' % (stock_name)
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
    
query = 'DESC %s' % list(result[0].values())[0]
curs.execute(query)
result = curs.fetchall()
for r in result:
    print(r)

# Insert Data
query_base = "INSERT INTO %s (Date, Open, High, Low, Close, Volume)" % (stock_name) +  "VALUES ('%s', %f, %f, %f, %f, %i)"
for i in tqdm(range(len(stock_data))):
    date_data = str(stock_data.index[i])[:10]
    open_data = stock_data.iloc[i]['Open']
    high_data = stock_data.iloc[i]['High']
    low_data = stock_data.iloc[i]['Low']
    close_data = stock_data.iloc[i]['Close']
    volume_data = stock_data.iloc[i]['Volume']
    query = query_base % (date_data, open_data, high_data, low_data, close_data, volume_data)
    curs.execute(query)
conn.commit()
    
# Get data from Table
query = 'SELECT * FROM %s' % stock_name
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

# curs.execute('DROP TABLE IF EXISTS AAPL')
