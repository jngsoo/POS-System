
from PyQt5.QtWidgets import *
from MemberControl import MemberCtrl
from PayControl import PayCtrl

PayController = PayCtrl
payCtrl = PayController()

MemberController = MemberCtrl
memberCtrl = MemberController()


#결제 탭 관련 모듈
class Payment:

    # 메뉴 이름, 가격 return
    def NameAndPrice(self, row, col):
        name = self.cafeMenus[row][col]
        price = self.cafeMenus[row][col + 1]
        return (name, price)

    # 인자 menu가 테이블에 있는지 검사 (있다면 몇번째 줄에 있는지 return)
    def isMenuOnTable(self, menu):
        # 메뉴 테이블 (10줄) 모두 검사
        for i in range(10):

            # 메뉴 테이블 i번째 행에 어떠한 메뉴가 적혀있다면
            if self.paymentTable.item(i, 0) != None:

                # 메뉴 테이블 i번째 행에 적힌 메뉴가 menu 라면 몇번째 행인지 i를 return
                if self.paymentTable.item(i, 0).text() == menu:
                    return i
        return False

    def HowManyOnMenuTable(self, row):
        return int(self.paymentTable.item(row, 1).text())

    # 메뉴 버튼 액션 -> payment테이블에 메뉴 이름과 가격 출력
    def writeOnTable(self, name, price):

        # paymentTable에 해당 메뉴가 없을 시에만 해당 메뉴 찍히도록
        if type(self.isMenuOnTable(name)) == bool and self.isMenuOnTable(name) == False:
            amount = 1

            for i in range(10):
                if self.paymentTable.item(i, 0) != None:
                    if self.paymentTable.item(i, 0).text() == ' ':
                        self.paymentTable.setItem(i, 0, QTableWidgetItem(name))  # 메뉴
                        self.paymentTable.setItem(i, 1, QTableWidgetItem(str(amount)))  # 수량
                        self.paymentTable.setItem(i, 2, QTableWidgetItem(str(price)))  # 금액
                        self.paymentTable.setItem(i, 3, QTableWidgetItem(amount * str(price)))  # 합계
                        self.totalAmount += amount
                        self.totalPrice += price
                        break

        # paymentTable에 해당 메뉴가 이미 있다면 수량,가격만 늘림
        else:

            i = self.isMenuOnTable(name)
            amount = int(self.HowManyOnMenuTable(i))
            amount += 1
            self.paymentTable.setItem(self.isMenuOnTable(name), 1, QTableWidgetItem(str(amount)))  # 수량
            self.paymentTable.setItem(self.isMenuOnTable(name), 3, QTableWidgetItem(str(amount * price)))  # 합계
            self.totalAmount += 1
            self.totalPrice += price

        self.showPriceTable()

    # 전체 메뉴 삭제 버튼과 연결
    def deleteAll(self):
        self.totalAmount = 0
        self.totalPrice = 0
        self.paid = 0
        self.totalRows = 0
        self.cardPaid, self.cashPaid, self.pointPaid = [], [], []  #

        # paymentTable 모두 초기화
        for i in range(10):
            self.paymentTable.setItem(i, 0, QTableWidgetItem(' '))
            self.paymentTable.setItem(i, 1, QTableWidgetItem(' '))
            self.paymentTable.setItem(i, 2, QTableWidgetItem(' '))
            self.paymentTable.setItem(i, 3, QTableWidgetItem(' '))

        # priceTable 모두 초기화
        self.priceTable.setItem(0, 0, QTableWidgetItem(' '))  # 총수량
        self.priceTable.setItem(0, 1, QTableWidgetItem(' '))  # 결제해야 할 금액
        self.priceTable.setItem(0, 2, QTableWidgetItem(' '))  # 결제한 금액

        self.Rrow = 0

    # 아래 3개 함수(payBy~)는 각각 카드 결제, 현금 결제, 포인트 결제와 연결지을 함수(팝업창 생성 후 데이터 입력받아 전달)
    def payByCard(self):
        defaultNum = self.totalPrice - self.paid
        i, okPressed = QInputDialog.getInt(self, "카드 결제", "금액: ", defaultNum, 0, 1000000, 1)
        if okPressed:

            if i < self.totalPrice - self.paid:
                self.paid += int(i)
                self.cardPaid.append(i)
                self.priceTable.setItem(0, 2, QTableWidgetItem(str(self.paid)))
                self.payComplete = False
            elif i == self.totalPrice - self.paid:
                self.cardPaid.append(i)
                alertMessage = str(self.totalPrice) + "원 결제가 완료되었습니다"
                QMessageBox.about(self, "띠용", alertMessage)

                self.payComplete = True
                #
                self.fin_pay()

                self.deleteAll()

            else:
                alertMessage = "결제 금액을 초과했습니다!\n남은 금액: " + str(self.totalPrice - self.paid) + "원"
                QMessageBox.about(self, "띠용", alertMessage)

    def payByCash(self):
        defaultNum = self.totalPrice - self.paid
        i, okPressed = QInputDialog.getInt(self, "현금 결제", "금액: ", defaultNum, 0, 1000000, 1)
        if okPressed:

            if i < self.totalPrice - self.paid:
                self.paid += int(i)
                self.cashPaid.append(i)
                self.priceTable.setItem(0, 2, QTableWidgetItem(str(self.paid)))
                self.payComplete = False

            elif i == self.totalPrice - self.paid:
                self.cashPaid.append(i)
                alertMessage = str(self.totalPrice) + "원 결제가 완료되었습니다"
                QMessageBox.about(self, "띠용", alertMessage)

                self.payComplete = True

                self.fin_pay()

                self.deleteAll()
            else:
                alertMessage = "결제 금액을 초과했습니다!\n남은 금액: " + str(self.totalPrice - self.paid) + "원"
                QMessageBox.about(self, "띠용", alertMessage)

    def payByPoint(self):

        # 결제 남은 금액
        defaultNum = self.totalPrice - self.paid
        # 포인트 결제 위해 멤버십(전화번호) 검색
        phoneNum, okPressed = QInputDialog.getText(self, "멤버십 조회", "전화번호: ( - 없이 전화번호만 입력 )", QLineEdit.Normal, "")

        if phoneNum in self.realMembers:

            i, okPressed = QInputDialog.getInt(self, "포인트 결제", "금액: ", defaultNum, 0, 1000000, 1)

            # 기입한 i에 비해 멤버의 잔여 포인트가 부족할 시
            if self.realMembers[phoneNum] < i:
                QMessageBox.about(self, "popup", "포인트가 부족합니다.")

            # 기입한 i가 멤버의 잔여 포인트로 해결 가능
            else:
                if okPressed:

                    if i < self.totalPrice - self.paid:
                        self.paid += int(i)
                        self.pointPaid.append(i)
                        self.priceTable.setItem(0, 2, QTableWidgetItem(str(self.paid)))

                        # 해당 멤버 포인트 삭감 및 멤버 테이블에 표시
                        # self.realMembers[phoneNum] -= int(i)
                        editedPoint = self.realMembers[phoneNum] - int(i)
                        memberCtrl.update_obj(phoneNum, editedPoint)
                        self.showMemberTable()

                        self.payComplete = False

                    elif i == self.totalPrice - self.paid:
                        self.pointPaid.append(i)
                        # self.realMembers[phoneNum] -= int(i)
                        alertMessage = str(self.totalPrice) + "원 결제가 완료되었습니다"
                        QMessageBox.about(self, "띠용", alertMessage)

                        # 해당 멤버 포인트 삭감 및 멤버 테이블에 표시
                        self.realMembers[phoneNum] -= int(i)
                        editedPoint = self.realMembers[phoneNum] - int(i)
                        memberCtrl.update_obj(phoneNum, editedPoint)
                        self.showMemberTable()

                        self.payComplete = True
                        self.fin_pay()
                        self.deleteAll()
                    else:
                        alertMessage = "결제 금액을 초과했습니다!\n남은 금액: " + str(self.totalPrice - self.paid) + "원"
                        QMessageBox.about(self, "띠용", alertMessage)

        else:
            QMessageBox.about(self, "popup", "조회된 멤버십이 없습니다.")

    ################PAYMENT MODULE#################

    def count_rows(self):
        for i in range(0, 10):
            if self.paymentTable.item(i, 0).text() != ' ':
                self.totalRows += 1
            else:
                break

    def fin_pay(self):
        self.count_rows()

        # pmenu 구성
        pmenu = ''
        for i in range(0, self.totalRows):
            name_buf = self.paymentTable.item(i, 0).text()
            name = payCtrl.clean_name(name_buf)
            size = self.paymentTable.item(i, 1).text()
            elm = [name, size]
            pmenu += '%s:%s,' % (name, size)
            self.this_pay.append(elm)

        # 거래번호 가져오기
        pnumb = payCtrl.get_numb()

        # paymethod 처리
        total_card, total_cash, total_point = 0, 0, 0
        if self.cardPaid != []:
            for elm in self.cardPaid:
                total_card += elm
        if self.cashPaid != []:
            for elm in self.cashPaid:
                total_cash += elm
        if self.pointPaid != []:
            for elm in self.cashPaid:
                total_point += elm
        pmethod = '%d,%d,%d' % (total_card, total_cash, total_point)

        for i in range(0, len(self.this_pay)):  # 재고 자동차감
            for j in range(0, int(self.this_pay[i][1])):
                payCtrl.sub_stocks(self.this_pay[i][0])

        payCtrl.add_payment(self.totalAmount, self.totalPrice,
                            pnumb, pmethod, self.date)
        payCtrl.add_payinfo(pnumb, self.date, pmenu)

    ################PAYMENT MODULE ENDS#################

    # 결제 탭 총수량 및 결제해야 할 금액 출력 함숫
    def showPriceTable(self):
        CurrentTotalPrice = 0
        CurrentTotalAmount = 0

        for i in range(10):
            if self.paymentTable.item(i, 3) != None and self.paymentTable.item(i, 3).text() != ' ':
                CurrentTotalPrice += int(self.paymentTable.item(i, 3).text())
                CurrentTotalAmount += int(self.paymentTable.item(i, 1).text())

        self.priceTable.setItem(0, 0, QTableWidgetItem(str(CurrentTotalAmount)))  # 총수량
        self.priceTable.setItem(0, 1, QTableWidgetItem(str(CurrentTotalPrice)))  # 결제해야 할 금액

    # 메뉴 수량 변경 버튼과 연결지을 함수
    def editAmount(self):
        # Rrow 는 테이블에서 선택된 메뉴의 줄(첫번째 줄은 0이고 1,2,3,...)
        Rrow = self.paymentTable.currentRow()

        # 빈칸을 선택한게 아니라면 활성화
        if self.paymentTable.currentItem() != None and self.paymentTable.item(Rrow, 0).text() != ' ':
            defaultAmount = int(self.paymentTable.item(Rrow, 1).text())
            i, okPressed = QInputDialog.getInt(self, "메뉴 수량 변경", "수량: ", defaultAmount, 0, 1000000, 1)
            self.paymentTable.setItem(Rrow, 1, QTableWidgetItem(str(i)))
            currentMenuPrice = int(self.paymentTable.item(Rrow, 2).text())
            self.paymentTable.setItem(Rrow, 3, QTableWidgetItem(str(i * currentMenuPrice)))

            # 변경 된 수량이 변경 전 수량보다 클 때 (가격이 증가)
            if i > defaultAmount:
                self.totalPrice += (i - defaultAmount) * int(self.paymentTable.item(Rrow, 2).text())

            # 변경 된 수량이 변경 전 수량보다 클 때 (가격이 증가)
            elif i < defaultAmount:
                self.totalPrice -= (defaultAmount - i) * int(self.paymentTable.item(Rrow, 2).text())

            self.showPriceTable()

    # 선택 메뉴 삭제 버튼과 연결지을 함수
    def removeOnTable(self):
        # Rrow 는 테이블에서 선택된 메뉴의 줄(첫번째 줄은 0이고 1,2,3,...)
        Rrow = self.paymentTable.currentRow()

        # 빈칸을 선택한게 아니라면 활성화
        if self.paymentTable.currentItem() != None and self.paymentTable.item(Rrow, 1).text() != ' ':
            # 데이터 변동
            menuAmount = int(self.paymentTable.item(Rrow, 1).text())
            menuPrice = int(self.paymentTable.item(Rrow, 2).text()) * menuAmount

            self.totalPrice -= menuPrice
            self.totalAmount -= menuAmount

            # 테이블 상에서 글자 지움
            self.paymentTable.setItem(Rrow, 0, QTableWidgetItem(' '))
            self.paymentTable.setItem(Rrow, 1, QTableWidgetItem(' '))
            self.paymentTable.setItem(Rrow, 2, QTableWidgetItem(' '))
            self.paymentTable.setItem(Rrow, 3, QTableWidgetItem(' '))

            # priceTable 변경
            self.showPriceTable()

        self.paymentTable.item(0, 3).text()