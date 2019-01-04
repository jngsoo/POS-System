from PyQt5.QtWidgets import *
from AccControl import AccCtrl
import datetime

AccountController = AccCtrl
accCtrl = AccountController()

class Account:

    def showAccounts(self):
        self.clearAcc()
        self.clearMini()
        date = datetime.datetime.now()
        curtime = date.strftime('%Y-%m-%d')
        curmonth = date.strftime('%Y-%m-')

        output_buf_1 = accCtrl.get_data_day(curtime)
        output_buf_2 = accCtrl.get_data_day_method(curtime)
        acc_amount = accCtrl.get_amount(curtime)
        upper_day = accCtrl.get_method_day(curtime)
        upper_month = accCtrl.get_method_month(curmonth)

        day_total_selling = accCtrl.get_day_total(curtime)
        self.acc_upper.setItem(0, 0, QTableWidgetItem(str(day_total_selling)))
        month_total_selling = accCtrl.get_month_total(curmonth)
        self.acc_upper.setItem(0, 1, QTableWidgetItem(str(upper_day[0])))
        self.acc_upper.setItem(0, 2, QTableWidgetItem(str(upper_day[1])))
        self.acc_upper.setItem(0, 3, QTableWidgetItem(str(upper_day[2])))

        self.acc_upper.setItem(1, 0, QTableWidgetItem(str(month_total_selling)))
        self.acc_upper.setItem(1, 1, QTableWidgetItem(str(upper_month[0])))
        self.acc_upper.setItem(1, 2, QTableWidgetItem(str(upper_month[1])))
        self.acc_upper.setItem(1, 3, QTableWidgetItem(str(upper_month[2])))

        for i in range(0, acc_amount):
            self.acc_main.setItem(i, 0, QTableWidgetItem(str(output_buf_1[i][0])))
            self.acc_main.setItem(i, 1, QTableWidgetItem(str(output_buf_2[i][0])))
            self.acc_main.setItem(i, 2, QTableWidgetItem(str(output_buf_1[i][1])))


    def clearAcc(self):
        for i in range(0, 50):
            for j in range(0, 3):
                self.acc_main.setItem(i, j, QTableWidgetItem(" "))

    def clearMini(self):
        for i in range(0, 3):
            self.acc_day_table.setItem(0, i, QTableWidgetItem(" "))


    def selectShow(self):
        c_date = self.calendarWidget.selectedDate()
        c_date = str(c_date.toPyDate())
        output1 = accCtrl.get_data_day(c_date)
        output2 = accCtrl.get_data_day_method(c_date)
        output_amount = accCtrl.get_amount(c_date)

        self.clearAcc()
        for i in range(0, output_amount):
            self.acc_main.setItem(i, 0, QTableWidgetItem(str(output1[i][0])))
            self.acc_main.setItem(i, 1, QTableWidgetItem(str(output2[i][0])))
            self.acc_main.setItem(i, 2, QTableWidgetItem(str(output1[i][1])))
        self.acc_main.resizeColumnsToContents()

        self.clearMini()
        selected_day = accCtrl.get_method_day(c_date)
        self.acc_day_table.setItem(0, 0, QTableWidgetItem(str(selected_day[3])))
        self.acc_day_table.setItem(0, 1, QTableWidgetItem(str(selected_day[0])))
        self.acc_day_table.setItem(0, 2, QTableWidgetItem(str(selected_day[1])))
        self.acc_day_table.setItem(0, 3, QTableWidgetItem(str(selected_day[2])))

