# db에 연결
def connectTOdb():
    import pymysql
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

# db에서 db 목록 조회
def showDB():
    import pymysql
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

# db에서 table 목록 조회
def showTB():
    import pymysql
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

# table view 
def viewTable():
    import pymysql
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

# table 다운로드
def downloadTB():
    import pymysql
    ip = 'snuro-db.p-e.kr'
    conn = pymysql.connect(host=ip, port=3306, user='SNURO', password='SNURO2022',
                        db='mysql', charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    curs = conn.cursor()

def whileDB():
    while True:
         
        c = input("원하는 번호를 입력하세요\n", "1 : DB 연결\n", "2 : DB 목록 조회\n", \
            "3 : DB 선택 후 조회\n", "4 : DB 다운로드\n", "5 : TABLE 목록 조회\n", "6 : TABLE 선택 후 조회\n", "7 : TABLE 다운로드\n", "8 : 이전으로 돌아가기\n", "9: QUIT\n")
        c = int(c)
        
        if int(c) == '9':
            break
        if c == 'q':
            break
        if c == 'q':
            break
        if c == 'q':
            break
        if c == 'q':
            break
    print("DB 연결이 해제되었습니다")
    return