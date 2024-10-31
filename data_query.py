from link import * #MySQL과 연결하는 함수 가져오기

#MySQL과 연결, 커서 가져옴
conn=create_connection()

#전체 메뉴, 이미지경로, 가격 가져오기
def menu_price_path():
    #conn에 대한 cursor를 만드는 함수
    cur= cursor(conn)
    #Query
    query="select path.menu_name,data.가격,path.img_path from drinks_img_path path join data data on path.id=data.no"
    
    cur.execute(query) #Query 실행

    #결과를 가져옴(열의 데이터가 튜플로 반환)
    result_tuples = cur.fetchall()

    #튜플 -> 리스트 변환
    result_list=[list(row) for row in result_tuples]

    #커서 종료
    cur.close()
    return result_list

''' 사용 예시
a= menu_price_path()
print(a)
'''