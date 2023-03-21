from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.settings import *
from src.profileDialog import ProfileDialog
from src.loginDialog import LoginDialog
from src.signupDialog import SignUpDialog
from src.noticeDialog import NoticeDialog
from src.newroomDialog import NewRoomDailog


class MainDialog(QWidget):
    def __init__(self):
        super(MainDialog, self).__init__()
        settings.initialInfo()
        self.setupUI()

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(MainDialog, self).keyPressEvent(event)

    def setupUI(self):
        self.resize(520, 360)
        self.setWindowTitle("BOSWU 보슈 :: 메인")
        self.setWindowIcon(QIcon(settings.img_path + "icon.png"))
        
        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        # small font
        self.smallfont = QFont()
        self.smallfont.setPointSize(10)
        self.smallfont.setBold(False)
        self.smallfont.setWeight(75)

        # basic font
        self.basicfont = QFont()
        self.basicfont.setPointSize(12)
        self.basicfont.setBold(False)
        self.basicfont.setWeight(75)
        self.basicfont.setFamily("맑은 고딕")

        # median font
        self.medianfont = QFont()
        self.medianfont.setPointSize(14)
        self.medianfont.setBold(False)
        self.medianfont.setWeight(75)
        self.medianfont.setFamily("맑은 고딕")

        # large font
        self.largefont = QFont()
        self.largefont.setPointSize(18)
        self.largefont.setBold(True)
        self.largefont.setWeight(75)
        self.largefont.setFamily("맑은 고딕")

        # label for header logo
        self.headerLable = QLabel()
        self.headerLable.setPixmap(QtGui.QPixmap(settings.img_path + "logo.png"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed) # 너비 확장 높이 확장
        self.headerLable.setSizePolicy(sizePolicy)
        self.headerLable.setAlignment(QtCore.Qt.AlignCenter)

        # button for login
        self.loginBtn = QPushButton("로그인하러 가기")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding) # 너비 확장 높이 확장
        self.loginBtn.setMaximumSize(400, 60)
        self.loginBtn.setSizePolicy(sizePolicy)
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.loginBtn.setFont(font)
        self.loginBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.loginBtn.setStyleSheet("background-color : #07A3B7;\n"
                                    "color : #FFF;\n"
                                    "border-radius : 10px;\n")
        self.loginBtn.clicked.connect(self.loginBtnClicked)

        # label for signupBox
        self.signupLabel = QLabel("BOSWU에 처음이신가요?")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.signupLabel.setFixedWidth(150)
        self.signupLabel.setSizePolicy(sizePolicy) # 너비 고정 높이 확장
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(75)
        self.signupLabel.setFont(font)
        self.signupLabel.setAlignment(QtCore.Qt.AlignLeft) # 왼쪽 정렬
        self.signupLabel.setAlignment(QtCore.Qt.AlignVCenter) # 수직 가운데 정렬
        self.signupLabel.setStyleSheet("color: #07A3B7;\n")
        # button for signupBox
        self.signupBtn = QPushButton("회원가입하러 가기")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.signupBtn.setFont(font)
        self.signupBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.signupBtn.setStyleSheet("color : #07A3B7;\n")
        self.signupBtn.clicked.connect(self.signupBtnClicked)

        self.outline = QVBoxLayout(self)
        self.outline.setSpacing(15)
        self.outline.setContentsMargins(30, 30, 30, 30)
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.tableBox = QHBoxLayout()
        self.tableBox.setAlignment(Qt.AlignLeft)

        self.btnBox = QVBoxLayout()
        self.btnBox.setContentsMargins(0, 15, 0, 15)
        self.btnBox.setSpacing(15)
        self.btnBox.setAlignment(Qt.AlignCenter)
        self.signupBox = QHBoxLayout()
        self.signupBox.setAlignment(Qt.AlignCenter)
        
        self.outline.addLayout(self.headerLayout)
        self.headerLayout.addWidget(self.headerLable)
        self.outline.addLayout(self.mainLayout)
        self.mainLayout.addLayout(self.tableBox)
        self.mainLayout.addLayout(self.btnBox)
        self.btnBox.addWidget(self.loginBtn)
        self.btnBox.addLayout(self.signupBox)
        self.signupBox.addWidget(self.signupLabel)
        self.signupBox.addWidget(self.signupBtn)

    def profileBtnClicked(self):
        self.close()
        dlg = ProfileDialog()
        dlg.exec_()
        self.show()

    def signupBtnClicked(self):
        self.close()
        dlg = SignUpDialog()
        dlg.exec_()
        self.show()
    
    def examBtnClicked(self):
        self.close()
        dlg = NoticeDialog()
        dlg.exec_()
        self.show()

    def loginBtnClicked(self):
        self.close()
        dlg = LoginDialog()
        dlg.exec_()
        
        if settings.login != False:
            self.updateUI()
        else:
            pass
        
        self.show()

    def updateUI(self):
        self.resize(760, 360)
        self.loginBtn.setParent(None)
        self.signupBox.setParent(None)
        self.signupLabel.setParent(None)
        self.signupBtn.setParent(None)
        settings.setInfo()

        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        # button for profile
        pixmap = QPixmap(settings.img_path + "profile.png")
        icon = QIcon()
        icon.addPixmap(pixmap)
        self.profileBtn = QPushButton()
        self.profileBtn.setIcon(icon)
        self.profileBtn.setIconSize(QSize(30, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) # 너비 고정 높이 고정
        self.profileBtn.setFixedWidth(30) # 너비 고정
        self.profileBtn.setFixedHeight(30) # 높이 고정
        self.profileBtn.setSizePolicy(sizePolicy)
        self.profileBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.profileBtn.setStyleSheet("border-radius : 15px;\n"
                                      "border : 0px;\n")
        self.profileBtn.clicked.connect(self.profileBtnClicked)

        self.idLabel = QLabel(settings.email)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.idLabel.setFixedHeight(30)
        self.idLabel.setSizePolicy(sizePolicy)
        self.idLabel.setFont(font)

        # button for make room
        self.newroomBtn = QPushButton("방 생성")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.newroomBtn.setMinimumSize(150, 60)
        self.newroomBtn.setMaximumSize(300, 120)
        self.newroomBtn.setSizePolicy(sizePolicy)
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.newroomBtn.setFont(font)
        self.newroomBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.newroomBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.newroomBtn.clicked.connect(self.newroomBtnClicked)

        # button for exam dialog
        self.goexamBtn = QPushButton("카메라 테스트")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.goexamBtn.setMinimumSize(150, 60)
        self.goexamBtn.setMaximumSize(300, 120)
        self.goexamBtn.setSizePolicy(sizePolicy)
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.goexamBtn.setFont(font)
        self.goexamBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.goexamBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.goexamBtn.clicked.connect(self.examBtnClicked)

        # button for logout
        self.logoutBtn = QPushButton("로그아웃")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.logoutBtn.setMinimumSize(150, 60)
        self.logoutBtn.setMaximumSize(300, 120)
        self.logoutBtn.setSizePolicy(sizePolicy)
        font.setPointSize(14)
        self.logoutBtn.setFont(font)
        self.logoutBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.logoutBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.logoutBtn.clicked.connect(self.logoutBtnClicked)


        self.roomPath = settings.db.child("rooms").child("current").child(settings.uid)
        self.rooms = self.roomPath.get()
        self.stream = self.roomPath.stream(self.stream_handler)

        # table for timeTable
        self.timeTable = QTableWidget()
        self.timeTable.setFont(self.basicfont)
        self.timeTable.setRowCount(len(self.rooms.val()))
        self.timeTable.setColumnCount(4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.timeTable.setMinimumSize(320, 200)
        self.timeTable.setSizePolicy(sizePolicy)
        self.timeTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # 수평 스크롤바
        #self.timeTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # 수직 스크롤바
        self.timeTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # 수정 불가능
        self.timeTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection) # 선택 불가능
        self.timeTable.setShowGrid(False) # 그리드 해제
        self.timeTable.setCornerButtonEnabled(False) # 코너 버튼 불가능
        self.timeTable.horizontalHeader().setVisible(True) # 수평 머리말
        self.timeTable.horizontalHeader().setStretchLastSection(True)
        self.timeTable.verticalHeader().setVisible(False) # 수직 머리말
        self.timeTable.setStyleSheet(#"background-color : qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(7, 163, 183, 255), stop:1 rgba(218, 235, 199, 255));\n"
                                        "color : white;\n"
                                        "border-radius : 10px;\n"
                                        "padding : 10px;\n")
        header = self.timeTable.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
        
        
        item = QTableWidgetItem("방 ID")
        self.timeTable.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem("과목명")
        self.timeTable.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem("분반")
        self.timeTable.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem("일시")
        self.timeTable.setHorizontalHeaderItem(3, item)

        i = 0
        for room in self.rooms.each():
            item = QTableWidgetItem(room.key())
            self.timeTable.setItem(i, 0, item)
            item = QTableWidgetItem(room.val()["subject"])
            self.timeTable.setItem(i, 1, item)
            item = QTableWidgetItem(str(room.val()["class num"]))
            item.setTextAlignment(Qt.AlignCenter)
            self.timeTable.setItem(i, 2, item)
            item = QTableWidgetItem(room.val()["test time"])
            self.timeTable.setItem(i, 3, item)
            i += 1


        self.headerLayout.addWidget(self.profileBtn)
        self.headerLayout.addWidget(self.idLabel)
        self.tableBox.addWidget(self.timeTable)

        if settings.admin == True:
            self.btnBox.addWidget(self.newroomBtn)

        self.btnBox.addWidget(self.goexamBtn)
        self.btnBox.addWidget(self.logoutBtn)

    def stream_handler(self, message):
        # We only care if something changed
        if message["event"] in ("put", "patch"):
            self.timeTable.clear()
            self.timeTable.setRowCount(len(self.rooms.val()))
            
            i = 0
            for room in self.rooms.each():
                item = QTableWidgetItem(room.key())
                self.timeTable.setItem(i, 0, item)
                item = QTableWidgetItem(room.val()["subject"])
                self.timeTable.setItem(i, 1, item)
                item = QTableWidgetItem(str(room.val()["class num"]))
                item.setTextAlignment(Qt.AlignCenter)
                self.timeTable.setItem(i, 2, item)
                item = QTableWidgetItem(room.val()["test time"])
                self.timeTable.setItem(i, 3, item)
                i += 1
        
    def logoutBtnClicked(self):
        settings.expireInfo()
        self.profileBtn.setParent(None)
        self.idLabel.setParent(None)
        self.timeTable.setParent(None)
        self.newroomBtn.setParent(None)
        self.goexamBtn.setParent(None)
        self.logoutBtn.setParent(None)
        
        self.btnBox.addWidget(self.loginBtn)
        self.btnBox.addLayout(self.signupBox)
        self.signupBox.addWidget(self.signupLabel)
        self.signupBox.addWidget(self.signupBtn)

    def newroomBtnClicked(self):
        self.close()
        dlg = NewRoomDailog()
        dlg.exec_()
        self.show()