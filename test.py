def total_price(): # order_table 으로 부터  총 가격 계산
    totalPrice = 0
    cur.execute("select * from order_table")
    while (True):
        row = cur.fetchone()
        if row == None:
            break
        order_id = row[0]
        data2 = row[3]
        data3 = row[4]
        totalPrice += data2 * data3
    return totalPrice
def add_order(order_1): #장바구니를 order_table (db) 에 저장 (영수증)
        #order=[1,'초코케이크',3,6000] #주문번호, 상품명, 갯수, 가격
        for i in range(len(order_1)):
            sql = "insert into order_table (id,customer_id,order_drink_name,order_drink,price,credit_card_id) values (%s,%s,%s,%s,%s,%s)"
            data = (order_1[i][0],order_1[i][1],order_1[i][2],order_1[i][3],order_1[i][4],order_1[i][5])
            cur.execute(sql,data)
            conn.commit()