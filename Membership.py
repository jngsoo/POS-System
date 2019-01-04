from PyQt5.QtWidgets import *
from MemberControl import MemberCtrl

MemberController = MemberCtrl
memberCtrl = MemberController()

#멤버십 탭 관련 모듈
class Membership:

    def showMemberTable(self):
        phoneNums = list(self.realMembers)
        memberPoints = list(self.realMembers.values())
        for i in range(len(phoneNums)):
            phoneNum = phoneNums[i]
            memberPoint = str(memberPoints[i])
            self.memberTable.setItem(i, 0, QTableWidgetItem(phoneNum))
            self.memberTable.setItem(i, 1, QTableWidgetItem(memberPoint))

    def editMember(self):
        # Rrow 는 테이블에서 선택된 메뉴의 줄(첫번째 줄은 0이고 1,2,3,...)

        Rrow = self.memberTable.currentRow()
        if self.memberTable.item(Rrow, 0) != None:
            phoneNum = self.memberTable.item(Rrow, 0).text()

        #어떠한 멤버 회원도 클릭 안되었을 시
        if Rrow == None:
            alertMessage = "수정할 멤버십 회원을 클릭해주세요"
            QMessageBox.about(self, "띠용", alertMessage)

        # 빈칸을 선택한게 아니라면 활성화
        if self.memberTable.item(Rrow,0) != None:
            if  self.memberTable.item(Rrow,0).text() != ' ':
                defaultPoint = int(self.memberTable.item(Rrow, 1).text())
                editingPoint, okPressed = QInputDialog.getInt(self, "멤버십 포인트 변경", phoneNum, defaultPoint,0,99999999999,1)

                if okPressed:
                    self.realMembers[phoneNum] = editingPoint
                self.memberTable.setItem(Rrow, 1, QTableWidgetItem(str(editingPoint)))
                self.realMembers[phoneNum] = editingPoint
                memberCtrl.update_obj(phoneNum, editingPoint)

            self.showMemberTable()

    def deleteMember(self):
        # Rrow 는 테이블에서 선택된 메뉴의 줄(첫번째 줄은 0이고 1,2,3,...)
        Rrow = self.memberTable.currentRow()
        if self.memberTable.item(Rrow,0) != None:
            phoneNum = self.memberTable.item(Rrow,0).text()

        # 빈칸을 선택한게 아니라면 활성화
        if self.memberTable.item(Rrow, 0) != None:
            if self.memberTable.item(Rrow, 0).text() != ' ':
                phoneNum = self.memberTable.item(Rrow, 0).text()
                del self.realMembers[phoneNum]
                memberCtrl.del_obj(phoneNum)
                alertMessage = str(phoneNum) + "삭제되었습니다."
                QMessageBox.about(self, "띠용", alertMessage)

        self.clearMemberTable()
        self.showMemberTable()

    def clearMemberTable(self):
        # 멤버십 테이블 모든 cell을 ' '로 초기화
        for i in range(22):
            for j in range(2):
                self.memberTable.setItem(i, j, QTableWidgetItem(' '))



    def membershipJoin(self):
        phoneNum, okPressed = QInputDialog.getText(self, "멤버십 가입", "전화번호(- 없이 번호만 입력해주세요): ", QLineEdit.Normal, "")

        if phoneNum == '':
            pass

        elif '-' in phoneNum:
            alertMessage = " - 을 제외한 전화번호를 입력해주세요"
            QMessageBox.about(self, "띠용", alertMessage)


        elif phoneNum not in self.realMembers:
            if okPressed:
                self.realMembers[phoneNum] = 0

            memberCtrl.set_obj(phoneNum, 0)
            self.showMemberTable()

            alertMessage = str(phoneNum) + " 가입되었습니다."
            QMessageBox.about(self, "띠용", alertMessage)

            self.memberTable.resizeColumnsToContents()

        else:
            alertMessage = str(phoneNum) + " 이미 가입된 번호입니다."
            QMessageBox.about(self, "띠용", alertMessage)

    def clearMlist(self):
        for i in range(30):
            for j in range(2):
                self.memberTable.setItem(i, j, QTableWidgetItem(" "))


    def searchMember(self):
        s_key = self.member_seach.toPlainText()
        result = memberCtrl.search_obj(s_key)
        self.clearMlist()
        for i in range(0, len(result)):
            self.memberTable.setItem(i, 0, QTableWidgetItem(str(result[i][0])))
            self.memberTable.setItem(i, 1, QTableWidgetItem(str(result[i][1])))

