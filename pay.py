import link as db
conn = db.create_connection()
cur=db.cursor(conn)
#임시 장바구니 구조 [id, 고객번호, 상품 이름, 상품 수량, 상품 가격, 카드 번호]
test_table=[[1,100,"아메리카노",1,2500,1234],[2,100,"카푸치노",2,3000,1234]]

#장바구니를 전달받아 데이터베이스 order_table에 저장하는 메서드
def add_cart(table):
    sql = "insert into order_table (id, customer_id, order_drink_name, order_drink,price,credit_card_id) values (%s, %s,%s, %s, %s, %s)"
    for i in range(len(table)):
        data=(table[i][0],table[i][1],table[i][2],table[i][3],table[i][4],table[i][5])
        cur.execute(sql,data)
        conn.commit()
#장바구니를 전달 받으면 총 결제 금액을 반환해주는 함수
def total_price(table):
    total=0
    for i in range(len(table)):
        total+=table[i][3] * table[i][4]

    return total

add_cart(test_table)
print("총 합 가격: ",total_price(test_table))