import pymysql
import mysql.connector
import pay as pay

order=[[1,'카라멜 마끼야또',3,2700],[1,'초코케이크',3,6000],[1,'아메리카노',2,2500]]
for i in [0,1,2]:
    pay.add_order(order[i])
    order.pop(0)
conn = pymysql.connect(host='localhost', user='jspuser', password='jsppass', db='jspdb', charset='utf8') #db연결
cur = conn.cursor()
def pay_request(orderid,total_price): #결제 정보(주문번호, 결제금액)를 저장하는 메서드
    sql = "insert into pay_request (order_num, total_price) values (%s, %s)"  #pay_request 테이블에 레코드 추가
    data=(orderid,total_price)
    cur.execute(sql,data)
    conn.commit()
    cur.execute("select * from pay_request")
    while(True):
        row=cur.fetchone()
        if row == None:
            break
        if orderid==row[0] and total_price==row[1]: #결제 정보가 제대로 저장되었는지 확인
            print("결제 정보 저장 성공")
        else:
            print("결제 정보 저장 실패")



total_price=0
order_id=0;
cur.execute("select * from test_order")
while(True):
    row=cur.fetchone()
    if row==None:
        break
    order_id=row[0]
    data2=row[2]
    data3=row[3]
    total_price+=data2*data3
print("총 결제 금액: ", total_price)
print("주문번호: ",order_id)
#pay_request(order_id,total_price)
conn.close()