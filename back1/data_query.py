from .link import * #MySQL과 연결하는 함수 가져오기

'''
#MySQL과 연결, 커서 가져옴
conn=create_connection()
'''

#리스트 /table (data join img_path) / [[메뉴이름, 가격,이미지경로,카테고리,품절여부(0/1)] ]
def get_menu_price_path_category(conn):
    try:
        #conn에 대한 cursor를 만드는 함수
        cur= cursor(conn)
        #Query
        query="""
                select path.menu_name,data.가격,path.img_path,data.분류,soldout.sold_out
                from drinks_img_path path 
                    join data data  on path.id=data.no
                    join drinks_sold_out soldout on path.id=soldout.id;
            
            """
                #형식: 메뉴이름, 가격, 이미지경로, 분류
        ##Query / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환
        cur.execute(query)
        result_tuple = cur.fetchall()
        result_list=[list(row) for row in result_tuple]
    except:
        print('get_menu_price_path_category ErrorOccured')
    finally:
        #커서 종료
        cur.close()
    return result_list

#리스트/ [[menu_name1],[menu_name2], ...]
def get_menu_name(conn):
    try:
        #conn에 대한 cursor를 만드는 함수
        cur= cursor(conn)
        #Query
        query="select 이름 from data"

        ##Query / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환
        cur.execute(query)
        result_list=[row[0] for row in cur.fetchall()]
    except:
        print('get_menu_name ErrorOccured')
    finally:
        #커서 종료
        cur.close()

    return result_list

#딕셔너리 {'메뉴':[  menu_price, [   옵션category, [옵션eng,옵션kor,opt_price]],  [옵션category2,[]]     ]    ], '메뉴2' }
def get_menu_option(conn):
    try:
        #conn에 대한 cursor를 만드는 함수
        cur= cursor(conn)
        menu = [item[0] for item in get_menu_price_path_category(conn)]

        #Query: 메뉴이름, 가격, 옵션들
        query_menu="""
                    select menu_name,price,
                            Addshot ,AddDeShot, ChangeStevia, AddStevia, ChangeLightVanila,
                            AddLightVanila, AddVanila, AddCaramel, SelectMilk ,AddHoney,
                            AddWhipping, AddCinnamon
                    from drinks_menu
                    """
        #Query: choose_id, eng_name, kor_name, add_price
        query_opt="select * from drinks_opt_price"

        #Query_Menu / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환    
        cur.execute(query_menu)
        menu_tuple = cur.fetchall()
        menu_list=[list(row) for row in menu_tuple]
        column_names = [i[0] for i in cur.description[2:]]

        #Query_Option / 튜플로 데이터 가져옴 / 튜플 -> 리스트 변환
        cur.execute(query_opt) 
        opt_tuple = cur.fetchall()
        opt_list=[list(row) for row in opt_tuple]

        # 불러온 옵션 넘버가 integer와 str으로 섞여있어서 검색이 어려움 ( 0,'1,2,3',0 이런식)
        #옵션리스트 -> 옵션 딕션너리로 변경

        opt_dict= {item[0]:[item[1],item[2],item[3]] for item in opt_list}
        
        #결과 딕셔너리
        res_dict={}
        #결과 딕셔너리 채우기
        for item in menu_list:
            key=item[0] #key는 앞의 메뉴명
            price = item[1]
            options_with_column_names = []

            for opt_name, opt_str in zip(column_names,item[2:]):
                opt = []
                if isinstance(opt_str, str):
                    opt_nums = opt_str.split(',')
                else:
                    opt_nums = [opt_str]
                
                for num in opt_nums:
                    if str(num).isdigit() and int(num) in opt_dict:
                        options_with_column_names.append(opt_name)
                        break
            res_dict[key] = [price, options_with_column_names]
        return res_dict
    
    except:
        print("get_menu_option(conn) ErrorOccured")
    finally:
        #커서 종료
        cur.close()


#리스트 /table data / [[no, 분류, 카테고리 번호, HOT/ICE, 이름, 가격, 설명] ]
def get_data(conn):
    try:
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
        return result_list
    except:
         print("get_data(conn) ErrorOccured")
    finally:
        #커서 종료
        cur.close()


#리스트/옵션 가격/ [[choose_id, eng_name,price],[] ]
def get_opt_price(conn):
    try:
        #conn에 대한 cursor를 만드는 함수
        cur= cursor(conn)

        #Query: choose_id, eng_name, kor_name, add_price
        query_opt="select * from drinks_opt_price"

        cur.execute(query_opt) 
        opt_tuple = cur.fetchall()
        opt_list=[list(row) for row in opt_tuple]
        opt= [[item[0],item[1],item[3]] for item in opt_list]
        return opt
    except:
         print("get_opt_price(conn) ErrorOccured")

    finally:
        #커서 종료
        cur.close()


# def(옵션이름,번호(opt_one)) => 값 반환
def get_opt_price(conn,name,num):
    try:
        #conn에 대한 cursor를 만드는 함수
        cur= cursor(conn)

        #Query
        query = "select opt_Name,opt_One,opt_Two,opt_Three from new_opt_data"

        cur.execute(query)
        opt_tuple = cur.fetchall()
        opt_list = [list(row) for row in opt_tuple]
        opt_dict = {item[0]:[item[1],item[2],item[3]] for item in opt_list}
        price = opt_dict[name][num]
    except:
        print("get_opt_price(conn,name,num) ErrorOccured")
    finally:
        #커서 종료
        cur.close()

    return price


#메뉴 설명 가져오기
def get_menu_info(conn,menu):
    try:
        #conn에 대한 cursor를 만드는 함수
        cur= cursor(conn)

        #Query
        query = "select menu_name, info from drinks_menu"

        cur.execute(query)
        menu_info_tuple = cur.fetchall()
        opt_dict= {item[0]:[item[1]] for item in menu_info_tuple}
    except:
        print("get_menu_info ErrorOccured")
    finally:
        #커서 종료
        cur.close()
    return opt_dict[menu]