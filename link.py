import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',        # 본인의 DB 사용자 이름으로 수정
            password = '0000', # 본인의 DB 비밀번호로 수정
            database = 'test_one',  # 본인의 DB 이름으로 수정
            port = 3303,
            auth_plugin='mysql_native_password'  # 인증 플러그인 명시
        )
        if conn.is_connected():  # 연결 성공 여부 확인
            print("MySQL 데이터베이스에 연결되었습니다.")
            return conn

    except Error as e:
        print(f"연결실패 : {e}")
        return None

def close_connection(conn):
    if conn.is_connected():
        conn.close()
        print("MySQL 데이터베이스와의 연결이 종료됨.")


