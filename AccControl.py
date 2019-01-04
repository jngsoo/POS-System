#

import pymysql

conn = pymysql.connect(host='45.119.147.76', user='root', password='201400867', db='hufPOS', charset='utf8')
curs = conn.cursor()

class AccCtrl:
    def get_data_day(self, date):
        try:
            key = "'" + date + "%'"
            curs.execute("""SELECT Ptime, Pmenu FROM t_payinfo
            WHERE Ptime LIKE %s""" % key)
            fetch_payment = curs.fetchall()
            return list(fetch_payment)
        except:
            print('error: searching by day failed')

    def get_day_total(self, date):
        try:
            key = "'" + date + "%'"
            curs.execute("""SELECT Pprice FROM t_payment
            WHERE Ptime LIKE %s""" % key)
            fetch_num = curs.fetchall()
            total_int = 0
            for i in range(0, len(fetch_num)):
                total_int += int(fetch_num[i][0])
            return total_int
        except:
            print('error:')

    def get_month_total(self, date):
        try:
            key = "'" + date + "%'"
            curs.execute("""SELECT Pprice FROM t_payment
            WHERE Ptime LIKE %s""" % key)
            fetch_num = curs.fetchall()
            total_int = 0
            for i in range(0, len(fetch_num)):
                total_int += int(fetch_num[i][0])
            return total_int
        except:
            print('error:')

    def get_method_day(self, date):
        try:
            key = "'" + date + "%'"
            curs.execute("""SELECT Pmethod FROM t_payment
            WHERE Ptime LIKE %s""" % key)
            fetch_method = curs.fetchall()

            card = 0
            cash = 0
            point = 0
            total = 0

            for i in range(0, len(fetch_method)):
                m_string = str(fetch_method[i])
                sp_buf = m_string[2:-3].split(',')
                card += int(sp_buf[0])
                cash += int(sp_buf[1])
                point += int(sp_buf[2])

            total = card + cash + point
            method_output = [card, cash, point, total]  # card, cash, point, total
            return method_output

        except:
            print('error:')



    def get_method_month(self, date):
        try:
            key = "'" + date + "%'"
            curs.execute("""SELECT Pmethod FROM t_payment
            WHERE Ptime LIKE %s""" % key)
            fetch_method = curs.fetchall()

            card = 0
            cash = 0
            point = 0
            total = 0

            for i in range(0, len(fetch_method)):
                m_string = str(fetch_method[i])
                sp_buf = m_string[2:-3].split(',')
                card += int(sp_buf[0])
                cash += int(sp_buf[1])
                point += int(sp_buf[2])

            total = card + cash + point
            method_output = [card, cash, point, total]  # card, cash, point, total
            return method_output

        except:
            print('error:')





    def get_data_day_method(self, date):
        try:
            key = "'" + date + "%'"
            curs.execute("""SELECT Pmethod FROM t_payment
            WHERE Ptime LIKE %s""" % key)
            fetch_payment = curs.fetchall()
            return list(fetch_payment)
        except:
            print('error: searching by day failed')

    def get_amount(self, date):
        try:
            key = "'" + date + "%'"
            curs.execute("""SELECT COUNT(*) FROM t_payinfo
            WHERE Ptime LIKE %s""" % key)
            fetch_amount = curs.fetchone()
            return fetch_amount[0]
        except:
            print('error: counting failed')
