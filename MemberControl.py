# pos project module 03
# Stock system: Controller
import pymysql
from Control import *

conn = pymysql.connect(host='45.119.147.76', user='root', password='201400867', db='hufPOS', charset='utf8')
curs = conn.cursor()


class MemberCtrl(Control):
    def set_obj(self, Mphone, Mpoint):
        # print('values:  %s, %s', Mphone, Mpoint)
        try:
            curs.execute("""INSERT INTO t_member (Mphone, Mpoint)
                VALUES (%s, %s)""",
                         (Mphone, Mpoint))
            conn.commit()
            # print(curs.lastrowid)
        except :
            print('there is wrong data, try again')

    def search_obj(self, Mphone):
        try:
            Mphone = "'%" + Mphone + "%'"
            curs.execute("""SELECT * FROM t_member WHERE Mphone LIKE %s""" % Mphone)
            src_result = curs.fetchall()
            # print(src_result)
            return list(src_result)
        except :
            print('there is wrong data, try again')

    def update_obj(self, Mphone, Mpoint):
        try:
            curs.execute("""UPDATE t_member SET Mpoint = %s WHERE Mphone = %s""",
                         (Mpoint, Mphone))
            conn.commit()
            # print(curs.lastrowid)
        except :
            print('there is wrong data, try again')

    def del_obj(self, Mphone):
        try:
            curs.execute("""DELETE FROM t_member WHERE Mphone = %s""",
                         Mphone)
            conn.commit()
            # print(curs.lastrowid)
        except :
            print('there is wrong data, try again')
