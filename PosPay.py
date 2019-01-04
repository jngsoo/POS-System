import pymysql
from PayControl import PayCtrl

conn = pymysql.connect(host='45.119.147.76', user='root', password='201400867', db='hufPOS', charset='utf8')
curs = conn.cursor()

PayController = PayCtrl
payCtrl = PayController()



