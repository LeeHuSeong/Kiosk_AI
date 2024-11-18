from datetime import datetime
import back1 as db

conn = db.create_connection()
table123=[['아메리카노',['샷 추가','옵션이름2','옵션이름3'],3,5000]
    ,['카푸치노',['샷 추가','옵션이름8','옵션이름7'],3,3000]
    ,['디카페인 아메리카노',[],3,4000]]

def add_receipt(order_id,table):
    cur=db.cursor(conn)
    price=0
    sql= ("insert into order_table2 ( customer_id, order_drink_name,opt_name, order_drink,price,pay_time) values (%s, %s,%s, %s, %s,%s)")
    for i in range(len(table)):
        str = ''
        for j in table123[i][1]:  # 옵션 합침
            str += j
            str += '/'
        #주문번호, 메뉴 이름, 적용 옵션, 수량, 가격, 결제 시간
        data=(order_id,table[i][0],str,table[i][2],table[i][3],datetime.now())
        price+=table[i][3]
        cur.execute(sql,data)
        conn.commit()
    cur.close()

add_receipt(101,table123)