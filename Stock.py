from PyQt5.QtWidgets import *
from StockControl import StoCtrl

StockController = StoCtrl
stoCtrl = StockController()

class Stock:

    # # # # # 2018 - 12 - 28 altered # # # # #
    def stock_clear(self):
        for i in range(30):
            for j in range(4):
                self.stock_table.setItem(i, j, QTableWidgetItem(' '))

    def s_search(self):
        self.stock_clear()
        s_key = self.stock_search_form.toPlainText()
        result = stoCtrl.search_obj(s_key)
        for i in range(0, len(result)):
            self.stock_table.setItem(i, 0, QTableWidgetItem(str(result[i][0])))
            self.stock_table.setItem(i, 1, QTableWidgetItem(str(result[i][1])))
            self.stock_table.setItem(i, 2, QTableWidgetItem(str(result[i][2])))
            self.stock_table.setItem(i, 3, QTableWidgetItem(str(result[i][3])))

    def showStockTable(self):
        self.stock_clear()
        output_buf = stoCtrl.get_data()
        stock_num = stoCtrl.get_amount()
        for i in range(0, stock_num):
            self.stock_table.setItem(i, 0, QTableWidgetItem(str(output_buf[i][0])))
            self.stock_table.setItem(i, 1, QTableWidgetItem(str(output_buf[i][1])))
            self.stock_table.setItem(i, 2, QTableWidgetItem(str(output_buf[i][2])))
            self.stock_table.setItem(i, 3, QTableWidgetItem(str(output_buf[i][3])))

    def addStock(self):
        Sname, okPressed = QInputDialog.getText(self, "재고 추가", "재고 이름: ", QLineEdit.Normal, "")
        Sstock, okPressed = QInputDialog.getText(self, "재고 추가", "재고 수량: ", QLineEdit.Normal, "")
        Sprice, okPressed = QInputDialog.getText(self, "재고 추가", "재고 단가: ", QLineEdit.Normal, "")

        if okPressed:
            stoCtrl.add_data(Sname, Sstock, Sprice)
            self.showStockTable()

    ### added modifying functions from here ###
    def modifyStock(self):
        Rrow = self.stock_table.currentRow()
        if self.stock_table.item(Rrow, 1) != None:
            Sitem = self.stock_table.item(Rrow, 1).text()

        # 빈칸을 선택한게 아니라면 활성화
        if self.stock_table.item(Rrow, 1) != None:
            if self.stock_table.item(Rrow, 0).text() != ' ':
                defaultAmount = int(self.stock_table.item(Rrow, 2).text())
                editingAmount, okPressed = QInputDialog.getText(self, "재고 수량 변경", "수량 입력: ", QLineEdit.Normal, "")

                if okPressed:
                    stoCtrl.update_obj(Sitem, editingAmount)
            self.showStockTable()
