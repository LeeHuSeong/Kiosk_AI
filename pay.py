import link as db
import random
conn = db.create_connection()
#임시 장바구니 구조 [id, 고객번호, 상품 이름, 상품 수량, 상품 가격, 카드 번호]
#임시 장바구니 [id, 고객번호, 상품 이름, 상품 수량, 상품 가격, 카드 번호]
test_table=[[1,100,"아메리카노",1,2500,1234],[2,100,"카푸치노",2,3000,1234]]
order_table=[] #메뉴이름, 수량, 가격 # 장바구니
#주문내역 [id, 고객번호, 상품 이름, 상품 수량, 상품 가격, 카드 번호] id = 음료 번호 , 고객 번호는 100부터 순차적 증

#장바구니를 전달받아 데이터베이스 order_table에 저장하는 메서드 장바구니 구조가 나중에 결정되면 거기에 맞춰서 변경
def add_cart(table):
    cur = db.cursor(conn)
    sql = "insert into order_table (id, customer_id, order_drink_name, order_drink,price,credit_card_id) values (%s, %s,%s, %s, %s, %s)"
    for i in range(len(table)):
        data=(table[i][0],table[i][1],table[i][2],table[i][3],table[i][4],table[i][5])
        cur.execute(sql,data)
        conn.commit()
        cur.close()

#장바구니를 전달 받으면 총 결제 금액을 반환해주는 함수
def total_price(table):
    total=0
    for i in range(len(table)):
        total+=table[i][1] * table[i][2]
    return total

# 메뉴 id, 옵션 id
# 이름 수량 가격
def cart(menu_id,opt_id,ea):
    table=[]
    table.insert(1,ea)
    cur = db.cursor(conn)
    sql = "select menu_name, price from menu_data where num=%s "
    data=(menu_id,)
    cur.execute(sql,data)
    row = cur.fetchone()
    table.insert(0,row[0])
    table.insert(2,row[1])
    for i in range(len(opt_id)):
        sql="select normal_drink from opt_price where choose_id = %s"
        data=(opt_id[i],)
        cur.execute(sql,data)
        row = cur.fetchone()
        table[2]=table[2]+row[0]
    return table
def a(table):
    test=table # 리스트 복제
#임시 장바구니로 테스트
#add_cart(test_table)
#print("결제 금액: ",total_price(test_table))
order_table.append(cart(1,[4,13],2)) # 2500 1700 2 > 4200
order_table.append(cart(3,[1],4)) # 4400 0 4
print(order_table)
print(total_price(order_table))
