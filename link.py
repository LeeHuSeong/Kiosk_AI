import mysql.connector

conn = mysql.connector.connect(
    host = "127.0.0.1:3303",
    user = "root",        # 본인의 DB 사용자 이름으로 수정
    password = "0000", # 본인의 DB 비밀번호로 수정
    database = "test_one"  # 본인의 DB 이름으로 수정
)

cursor= conn.cursor()
conn.commit()
conn.close()