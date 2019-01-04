import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *  # Qtimer (시간 알려주는) 쓰려고 import 햇다
from PyQt5 import uic
import pymysql

#각각 결제, 정산, 재고, 멤버십 관련 모듈
from Payment import *
from Account import *
from Stock import *
from Membership import *


conn = pymysql.connect(host='45.119.147.76', user='root', password='201400867', db='hufPOS', charset='utf8')
curs = conn.cursor()


class Memberinfo:
    def getdata(self):
        curs.execute("""SELECT * FROM t_member """)
        conn.commit()
        all_table = curs.fetchall()
        return all_table


libpaths = QApplication.libraryPaths()

form_class = uic.loadUiType("POS2.ui")[0]

class MyWindow(QMainWindow, form_class, Memberinfo, Payment, Account, Stock, Membership, ):
    # 메뉴 이름, 메뉴 가격, 메뉴 코드(M01 ~ M99), 재료(재고)
    # 추가지점
    this_pay = []
    date = datetime.datetime.now()
    date = date.strftime('%Y/%m/%d %H:%M')


    members = {'01012341234':5000, '01043214321':2000, '01098765432':2500}
    realMembers = {}

    this_member = Memberinfo()
    show_table = this_member.getdata()

    for i in range(len(show_table)):
        realMembers[show_table[i][0]] = show_table[i][1]




    cafeMenus = [['아메리카노', 3000], ['카페라떼', 4000], ['카페모카', 4500], ['카푸치노', 3500], ['카라멜\n마끼아또', 5000],
                 ['바닐라라떼', 4500], ['청포도\n에이드', 5000], ['자몽 에이드', 5000], ['아인슈패너', 6500], ['딸기 바나나\n에이드', 3500],
                 ['체리 에이드', 3500], ['딸기 바나나\n요거트', 3500], ['초코 바나나\n요거트', 3500], ['청포도 자몽\n요거트', 3500],
                 ['레몬 바나나\n요거트', 3500],
                 ['SHOT', 800], ['ICE', 500]
                 ]
    #GUI 화면 세팅
    def __init__(self):
        self.this_pay = []
        self.totalRows = 0
        self.date = datetime.datetime.now()
        self.date = self.date.strftime('%Y/%m/%d %H:%M')

        this_member = Memberinfo()
        show_table = this_member.getdata()

        # MyWindow가 상속받는 QMainWindow의 생성자 명시
        super().__init__()

        # 메뉴 이름, 메뉴 가격, 메뉴 코드(M01 ~ M99), 재료(재고)
        cafeMenus = [['아메리카노', 3000], ['카페라떼', 4000], ['카페모카', 4500], ['카푸치노', 3500], ['카라멜\n마끼아또', 5000],
                     ['바닐라라떼', 4500], ['청포도\n에이드', 5000], ['자몽 에이드', 5000], ['아인슈패너', 6500], ['딸기 바나나\n에이드', 3500],
                     ['체리 에이드', 3500], ['딸기 바나나\n요거트', 3500], ['초코 바나나\n요거트', 3500], ['청포도 자몽\n요거트', 3500],
                     ['레몬 바나나\n요거트', 3500],
                     ['SHOT', 800], ['ICE', 500]
                     ]

        # priceTable에 쓰일 변수들
        self.totalAmount = 0
        self.totalPrice = 0
        self.paid = 0

        # 각각 카드,현금,포인트 매출
        self.cardPaid = []
        self.cashPaid = []
        self.pointPaid = []

        # paymentTable에 메뉴가 출력될 행(초기값 0, 즉 첫번째 줄)
        self.Rrow = 0

        #결제 완료 bool value
        self.payComplete = False

        # 밑에 현재 시간나오는
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        self.setupUi(self)

        #메뉴 표시 테이블 모든 cell을 ' '로 초기화
        for i in range(11):
            for j in range(4):
                self.paymentTable.setItem(i, j , QTableWidgetItem(' '))

        #멤버십 테이블 모든 cell을 ' '로 초기화
        for i in range(22):
            for j in range(2):
                self.memberTable.setItem(i, j , QTableWidgetItem(' '))

        #재고 테이블 모든 cell을 ' '로 초기화
        for i in range(30):
            for j in range(4):
                self.stock_table.setItem(i, j, QTableWidgetItem(' '))


        self.showMemberTable()
        self.showStockTable()

        #추가함
        self.showAccounts()
        #추가끝

        # 테이블 열 크기 조정
        self.memberTable.resizeColumnsToContents()
        self.acc_main.resizeColumnsToContents()

        # 메뉴 버튼에 메뉴 이름 설정
        self.menuButton1_1.setText(cafeMenus[0][0])
        self.menuButton1_2.setText(cafeMenus[1][0])
        self.menuButton1_3.setText(cafeMenus[2][0])
        self.menuButton1_4.setText(cafeMenus[3][0])
        self.menuButton1_5.setText(cafeMenus[4][0])
        self.menuButton2_1.setText(cafeMenus[5][0])
        self.menuButton2_2.setText(cafeMenus[6][0])
        self.menuButton2_3.setText(cafeMenus[7][0])
        self.menuButton2_4.setText(cafeMenus[8][0])
        self.menuButton2_5.setText(cafeMenus[9][0])
        self.menuButton3_1.setText(cafeMenus[10][0])
        self.menuButton3_2.setText(cafeMenus[11][0])
        self.menuButton3_3.setText(cafeMenus[12][0])
        self.menuButton3_4.setText(cafeMenus[13][0])
        self.menuButton3_5.setText(cafeMenus[14][0])
        self.menuButton4_1.setText(cafeMenus[15][0])
        self.menuButton4_2.setText(cafeMenus[16][0])

        # 메뉴 버튼에 색(배경, 글씨) 설정
        # self.menuButton1_1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')

        # 메뉴 버튼 액션 설정 (1열)
        self.menuButton1_1.clicked.connect(lambda: self.writeOnTable(cafeMenus[0][0], cafeMenus[0][1]))
        self.menuButton1_2.clicked.connect(lambda: self.writeOnTable(cafeMenus[1][0], cafeMenus[1][1]))
        self.menuButton1_3.clicked.connect(lambda: self.writeOnTable(cafeMenus[2][0], cafeMenus[2][1]))
        self.menuButton1_4.clicked.connect(lambda: self.writeOnTable(cafeMenus[3][0], cafeMenus[3][1]))
        self.menuButton1_5.clicked.connect(lambda: self.writeOnTable(cafeMenus[4][0], cafeMenus[4][1]))

        # 메뉴 버튼 액션 설정 (2열)
        self.menuButton2_1.clicked.connect(lambda: self.writeOnTable(cafeMenus[5][0], cafeMenus[5][1]))
        self.menuButton2_2.clicked.connect(lambda: self.writeOnTable(cafeMenus[6][0], cafeMenus[6][1]))
        self.menuButton2_3.clicked.connect(lambda: self.writeOnTable(cafeMenus[7][0], cafeMenus[7][1]))
        self.menuButton2_4.clicked.connect(lambda: self.writeOnTable(cafeMenus[8][0], cafeMenus[8][1]))
        self.menuButton2_5.clicked.connect(lambda: self.writeOnTable(cafeMenus[9][0], cafeMenus[9][1]))

        # 메뉴 버튼 액션 설정 (3열)
        self.menuButton3_1.clicked.connect(lambda: self.writeOnTable(cafeMenus[10][0], cafeMenus[10][1]))
        self.menuButton3_2.clicked.connect(lambda: self.writeOnTable(cafeMenus[11][0], cafeMenus[11][1]))
        self.menuButton3_3.clicked.connect(lambda: self.writeOnTable(cafeMenus[12][0], cafeMenus[12][1]))
        self.menuButton3_4.clicked.connect(lambda: self.writeOnTable(cafeMenus[13][0], cafeMenus[13][1]))
        self.menuButton3_5.clicked.connect(lambda: self.writeOnTable(cafeMenus[14][0], cafeMenus[14][1]))

        # 메뉴 버튼 액션 설정 (4열)
        self.menuButton4_1.clicked.connect(lambda: self.writeOnTable(cafeMenus[15][0], cafeMenus[15][1]))
        self.menuButton4_2.clicked.connect(lambda: self.writeOnTable(cafeMenus[16][0], cafeMenus[16][1]))

        # 선택 메뉴 삭제 액션 설정
        self.deleteMenu.clicked.connect(self.removeOnTable)

        # 메뉴 수량 변경 액션 설정
        self.changeAmount.clicked.connect(self.editAmount)

        # 전체 메뉴 삭제 버튼 클릭 시 총 수량, 결제 금액, 결제한 금액 모두 0으로 초기화
        self.deleteAllMenus.clicked.connect(self.deleteAll)

        #카드 결제, 현금 결제, 포인트 결제 액션 설정
        self.payCard.clicked.connect(self.payByCard)
        self.payCash.clicked.connect(self.payByCash)
        self.payPoint.clicked.connect(self.payByPoint)

        #멤버십 가입 버튼 액션 설정
        self.memberJoin.clicked.connect(self.membershipJoin)

        #멤버십 수정 버튼 액션 설정
        self.memberEdit.clicked.connect(self.editMember)

        #멤버십 삭제 버튼 액션 설정
        self.memberDelete.clicked.connect(self.deleteMember)

        #재고 수정 버튼 액션 설정
        self.stock_modify.clicked.connect(self.modifyStock)

        #재고 추가 버튼 액션 설정
        self.stock_add.clicked.connect(self.addStock)

        #정산 조회 버튼 액션 설정
        self.acc_select_search.clicked.connect(self.selectShow)

        #정산 새로고침 액션 설정
        self.acc_refresh.clicked.connect(self.showAccounts)

        #재고 검색 버튼 액션 설정
        self.stock_search.clicked.connect(self.s_search)

        #재고 새로고침 액션 설정
        self.refresh_list.clicked.connect(self.showStockTable)

        #멤버십 검색 액션 설정
        self.go_msearch.clicked.connect(self.searchMember)

    #시계
    def timeout(self):
        cur_date = QDate.currentDate()
        str_date = cur_date.toString("MM월 dd일  ")
        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.timeLabel.setText(str_date + str_time)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()


