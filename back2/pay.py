import link as db
import random
conn = db.create_connection()
#임시 장바구니 구조 [id, 고객번호, 상품 이름, 상품 수량, 상품 가격, 카드 번호]
test_table=[[1,100,"아메리카노",1,2500,1234],[2,100,"카푸치노",2,3000,1234]]
order_table=[] #cart메서드  테스트용 리스트

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

# 메뉴 id , 옵션 id 수량을 주면 리스트 만들어서 반환
def cart(menu_id,opt_id,ea):
    table=[] #이름 수량 가격
    table.insert(1,ea)
    cur = db.cursor(conn)
    sql = "select menu_name, price from menu_data where num=%s " #menu_data db에서 id 검색해서 이름과 가격을 들고옴
    data=(menu_id,)
    cur.execute(sql,data)
    row = cur.fetchone()
    table.insert(0,row[0])
    table.insert(2,row[1])
    for i in range(len(opt_id)):
        sql="select normal_drink from opt_price where choose_id = %s" #opt_price에서 id 검색해서 가격을 들고옴
        data=(opt_id[i],)
        cur.execute(sql,data)
        row = cur.fetchone()
        table[2]=table[2]+row[0]
    cur.close()
    return table
def a(table): #추후 구현
    test=table # 리스트 복제
#임시 장바구니로 테스트
#add_cart(test_table)
#print("결제 금액: ",total_price(test_table))
order_table.append(cart(1,[4,13],2)) # 메뉴 id : 1 , 옵션 id : 4,13 , 수량 : 2
order_table.append(cart(3,[1],4)) # 메뉴 id : 1 , 옵션 id : 1 , 수량 : 2
print(order_table) # 만든 장바구니 출력
print(total_price(order_table)) #총 결제 금액 출력
