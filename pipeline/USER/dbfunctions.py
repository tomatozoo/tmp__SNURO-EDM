# db에 연결
import pandas as pd
import openpyxl

def connectTOdb():
    import pymysql
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()
    return curs

# db에서 db 목록 조회
def showDB(curs):
    query = 'SHOW DATABASES'
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)
        
# db에서 table 목록 조회
def showTB(curs):
    print("DB 목록은 다음과 같습니다")
    query = 'SHOW DATABASES'
    curs.execute(query)
    result = curs.fetchall()
    for r in result:
        print(r)  
          
    print("조회하고자 하는 DB 이름을 정확히 입력해주세요")
    dbname = input("DB NAME : ")
    query = f'USE {dbname}'
    try:
        curs.execute(query)
    except:
        print("ERROR")
        
    print(f"DB {dbname}의 table 목록입니다")
    sql = 'SHOW TABLES'
    curs.execute(sql)
    result = curs.fetchall()
    for r in result:
        print(r)
        
    return dbname

# table view 
def viewTable():
    import pymysql
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

# table 다운로드
def downloadTB(curs, dbname):
    print(f"DB {dbname}의 table 목록입니다")
    query = f'USE {dbname}'
    try:
        curs.execute(query)
    except:
        print("ERROR")
        
    sql = 'SHOW TABLES'
    curs.execute(sql)
    result = curs.fetchall()
    for r in result:
        print(r)
    
    print(f"DB {dbname}에서 조회/다운로드할 table 이름을 정확히 입력해주세요.")
    tbName = input("table name : ")    
    try:
        query = 'SELECT * FROM %s' % tbName
        curs.execute(query)
        result = curs.fetchall()
        df = pd.DataFrame(result)
        for r in result:
            print(r)
        
    except:
        print("ERROR")

    print("table을 다운로드할 파일 이름을 정해주세요 (ex. snuro_zoom_week1)")
    fileName = input("file name : ")
    df.to_excel(f'./{fileName}.xlsx')
    print("다운로드가 시작됩니다")
   
    
        
def whileDB():
    while True:
        c = input("원하는 번호를 입력하세요\n1 : DB 연결\n2 : DB 목록 조회\n3 : DB 선택 후 테이블 목록 조회\n4 : TABLE 조회/다운로드\n9: QUIT\n")

        
        if c == '1': # DB 연결 
            connectTOdb()
        
        if c == '2': # DB 목록 조회
            curs = connectTOdb()
            showDB(curs )
        
        if c == '3': # DB 선택 후 조회
            curs = connectTOdb()
            db = showTB(curs)
        if c == '4': # TB 목록 조회
            curs = connectTOdb()
            downloadTB(curs,db)
        if c == '9':
            break
    print("DB 연결이 해제되었습니다")
    return