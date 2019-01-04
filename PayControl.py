#

import pymysql

conn = pymysql.connect(host='45.119.147.76', user='root', password='201400867', db='hufPOS', charset='utf8')
curs = conn.cursor()


class PayCtrl:
    def clean_name(self, str):
        str1 = str.replace("\n", "")
        str2 = str1.replace(" ", "")
        return str2

    def get_numb(self):
        try:
            curs.execute("""SELECT COUNT(Pnumb) FROM t_payment""")
            fetch_numb = curs.fetchone()
            numb = fetch_numb[0] + 1
            return numb
        except:
            print('error: counting the next pay-number failed')
            return 1

    def add_payment(self, Pcount, Pprice, Pnumb, Pmethod, Ptime):
        print('values: %s, %s, %s, %s, %s', Pcount, Pprice, Pnumb, Pmethod, Ptime)
        try:
            curs.execute("""INSERT INTO t_payment
            VALUES (%s, %s, %s, %s, %s)""",
                             (Pcount, Pprice, Pnumb, Pmethod, Ptime))
            conn.commit()
            print(curs.lastrowid)
        except:
            print('error: adding payment data failed')

    def add_payinfo(self, Pnumb, Ptime, Pmenu):
        print('values: %s, %s, %s', Pnumb, Ptime, Pmenu)
        try:
            curs.execute("""INSERT INTO t_payinfo
                    VALUES (%s, %s, %s)""",
                         (Pnumb, Ptime, Pmenu))
            conn.commit()
            print(curs.lastrowid)
        except:
            print('error: adding payment information failed')

    def sub_stocks(self, MNname):
        print('value: %s', MNname)
        try:
            curs.execute("""SELECT MNstocks FROM t_product
            WHERE MNname = '%s'""" % MNname)
            stock_fetch = str(curs.fetchone())
            stock_buf = stock_fetch.split("'")[1]
            stock_pr = stock_buf.split(',')
            if len(stock_pr) == 2:
                if stock_pr[0] == '-':
                    pass
                else:
                    curs.execute("""
                    UPDATE t_stock
                    SET Sstock = Sstock -1
                    WHERE Sname = '%s'""" % stock_pr[0])
                    conn.commit()
            else:
                for i in range(0, len(stock_pr)):
                    curs.execute("""
                    UPDATE t_stock
                    SET Sstock = Sstock -1
                    WHERE Sname = '%s'""" % stock_pr[i])
                    conn.commit()
        except:
            print('error: subtracting corresponded stocks failed')



