from link import * #MySQL과 연결하는 함수 가져오기

#MySQL과 연결, 커서 가져옴
conn=create_connection()

#리스트 /table (data join img_path) / [[메뉴이름, 가격,이미지경로,카테고리] ]
def get_menu_price_path_category():
    #conn에 대한 cursor를 만드는 함수
    cur = cursor(conn)
    #Query
    query="""
            select path.menu_name,data.가격,path.img_path,data.분류
            from drinks_img_path path join data data on path.id=data.no
          """
            #형식: 메뉴이름, 가격, 이미지경로, 분류
    ##Query / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환
    cur.execute(query)
    result_tuple = cur.fetchall()
    result_list=[list(row) for row in result_tuple]

    #커서 종료
    cur.close()
    return result_list


#딕셔너리 /table (drinks_menu & drinks_opt_price) / {'메뉴':[옵션eng,옵션kor,가격] }
def get_menu_option():
    #conn에 대한 cursor를 만드는 함수
    cur = cursor(conn)

    #Query: 메뉴이름, 가격, 옵션들
    query_menu="""
                select menu_name,price,
                        cinnamon,whip,strong_or_weak,syrup_add,light_vanilia_add,
                        stevia_changed,stevia_add,honey_add,choose_milk
                from drinks_menu
                """
    #Query: choose_id, eng_name, kor_name, add_price
    query_opt="select * from drinks_opt_price"

    #Query_Menu / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환
    cur.execute(query_menu)
    menu_tuple = cur.fetchall()
    menu_list=[list(row) for row in menu_tuple]

    #Query_Option / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환
    cur.execute(query_opt) 
    opt_tuple = cur.fetchall()
    opt_list=[list(row) for row in opt_tuple]
    

    # 불러온 옵션 넘버가 integer와 str으로 섞여있어서 검색이 어려움 ( 0,'1,2,3',0 이런식)
    #옵션리스트 -> 옵션 딕션너리로 변경
    opt_dict= {item[0]: [item[1],item[2],item[3]] for item in opt_list}
    
    #결과 딕셔너리
    res_dict={}

    #결과 딕셔너리 채우기
    for item in menu_list:
        key=item[0] #key는 앞의 메뉴명
        opt=[] #밸류를 담음

        for opt_str in item[2:]:
            if isinstance(opt_str,str): #str타입인지
                #opt_nums는 리스트
                opt_nums=opt_str.split(',')
            else: 
                opt_nums=[opt_str]
            
            for num in opt_nums:
                #isdigit() = 숫자 판별 T/F
                if str(num).isdigit() and int(num) in opt_dict: 
                    opt.append(opt_dict[int(num)])
        
        #키(메뉴이름)에 맞는 밸류(옵션) 추가
        res_dict[key]=opt
    
    #커서 종료
    cur.close()
    return res_dict


#리스트 /table data / [[no, 분류, 카테고리 번호, HOT/ICE, 이름, 가격, 설명] ]
def get_data():
    #conn에 대한 cursor를 만드는 함수
    cur= cursor(conn)
    #Query
    query="""
            select * from data
          """
    #Query_* / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환
    cur.execute(query)
    result_tuple = cur.fetchall()
    result_list=[list(row) for row in result_tuple]

    #커서 종료
    cur.close()
    return result_list

    

'''
#menu_price_path_category 테스트
a= get_menu_price_path_category()
print(a)

#menu_option()테스트
b= get_menu_option()
print(b)
#딕셔너리라서 검색할 때, 아래처럼 써야함
print(b['아메리카노'])

#get_data 테스트
c= get_data()
print(c)
'''