#

import pymysql

conn = pymysql.connect(host='45.119.147.76', user='root', password='201400867', db='hufPOS', charset='utf8')
curs = conn.cursor()

class StoCtrl:
    def get_amount(self):
        try:
            curs.execute("""SELECT COUNT(Scode) FROM t_stock""")
            fetch_amount = curs.fetchone()
            amount = fetch_amount[0]
            return amount
        except:
            print('error: counting total amount of stocks failed')

    def get_data(self):
        try:
            curs.execute("""SELECT * FROM t_stock""")
            fetch_data = curs.fetchall()
            return(list(fetch_data))
        except:
            print('error: importing stock list failed')

    def add_data(self, Sname, Sstock, Sprice):
        try:
            new_Scode = 's' + str(int(self.get_amount()) + 1)
            curs.execute("""INSERT INTO t_stock
            VALUES (%s, %s, %s, %s)""",
                         (new_Scode, Sname, Sstock, Sprice))
            conn.commit()
            print(curs.lastrowid)
        except:
            print('error: adding new stock data failed')

    def search_obj(self, Sname):
        try:
            Sname = "%"+Sname+"%"
            print(Sname)
            curs.execute("""SELECT * FROM t_stock WHERE Sname LIKE %s""", Sname)
            conn.commit()
            src_result = curs.fetchall()
            print(src_result)
            return src_result
        except :
            print('there is wrong data, try again')


    def update_obj(self, Sname, Sstock):
        try:
            curs.execute("""UPDATE t_stock SET Sstock = %s WHERE Sname = %s""",
                         (Sstock, Sname))
            conn.commit()
            print(curs.lastrowid)
        except :
            print('there is wrong data, try again')

    def del_obj(self, Sname):
        try:
            curs.execute("""DELETE FROM t_stock WHERE Sname = %s""",
                         Sname)
            conn.commit()
            print(curs.lastrowid)
        except :
            print('there is wrong data, try again')