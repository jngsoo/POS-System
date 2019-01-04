# pos project module 03
# Stock system

import pymysql
from MemberControl import MemberCtrl

conn = pymysql.connect(host='45.119.147.76', user='root', password='201400867', db='hufPOS', charset='utf8')
curs = conn.cursor()
##########

MemberController = MemberCtrl
memberCtrl = MemberController()

class Memberinfo:
    def getdata(self):
        curs.execute("""SELECT * FROM t_member """)
        conn.commit()
        all_table = curs.fetchall()
        return all_table

   # def cal_netsales(self):
##########

# main
membernotdone = True


while membernotdone:
    command = ''
    addp = ''
    this_member = Memberinfo()
    show_table = this_member.getdata()
    '''for idx_i, val_i in enumerate(show_table):
        for idx_j, val_j in enumerate(val_i):
            print (val_j)'''
    print (show_table)
    print('select function')
    print('1) add Member into a Membertable')
    print('2) find Member')
    print('3) update Member')
    print('4) delete Member')
    command = input('type user command: ')

    if command == '1': # 1) add Member into a Membertable
        Mphone, Mpoint = map(str, input('다음을 차례로 입력하세요: 회원번호, 전화번호, 포인트\n').split(','))
        Mphone = Mphone.strip(',')
        print(Mphone, Mpoint)
        memberCtrl.set_obj(Mphone, Mpoint)
        set_result = curs.execute("""SHOW FULL COLUMNS FROM t_member """)
        print('the added member is:', set_result)
        print('\n\n\n')

    elif command == '2': # 2) find Member
        Mphone = input('검색하고자 하는 회원 전화번 호를 입력하세요:')
        print(Mphone)
        search_result = str(memberCtrl.search_obj(Mphone))
        search_result = search_result.strip('(())')
        print('검색결과:', search_result)
        print('\n\n\n')

    elif command == '3': # 3) update Member
        Mphone, Mpoint = map(str, input('수정하고자 하는 회원 전화번호, 포인트을 입력하세요:').split(','))
        Mphone = Mphone.strip(',')
        print(Mphone, Mpoint)
        memberCtrl.update_obj(Mphone, Mpoint)
        update_result = memberCtrl.search_obj(Mphone)
        print('수정결과:', update_result)
        print('\n\n\n')

    elif command == '4': # 4) delete Stock
        Mphone = input('삭제하고자 하는 회원 전화번호를 입력하세요:')
        memberCtrl.del_obj(Mphone)
        del_result = memberCtrl.search_obj(Mphone)
        print('삭제결과:', del_result)
        print('\n\n\n')

    else:
        print('unexpected command is detected')
        break

exit(1) #error exit
conn.close()

