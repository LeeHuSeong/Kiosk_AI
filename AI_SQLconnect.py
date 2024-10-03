import mysql.connector

# MySQL 데이터베이스 연결
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        #ID / Pass 맞춰서 수정
        user="root",
        password="rootpass",
        #DB 이름 정해지면 수정
        database="menu_db"
    )
    return connection

# 메뉴 주문 카운트 증가
def update_order_count(menu):
    conn = connect_to_db()
    cursor = conn.cursor()

    # 메뉴의 주문 횟수 증가
    query = "UPDATE orders SET count = count + 1 WHERE menu = %s"
    cursor.execute(query, (menu,))
    conn.commit()

    # 오늘의 몇 번째 주문인지 확인
    query_today = "SELECT SUM(count) FROM orders WHERE DATE(order_time) = CURDATE()"
    cursor.execute(query_today)
    order_count_today = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return order_count_today

# 선택된 메뉴 주문 카운트 업데이트 및 오늘의 주문 수 출력
if selected_menu:
    order_count_today = update_order_count(selected_menu)
    print(f"오늘의 {order_count_today}번째 주문입니다.")
