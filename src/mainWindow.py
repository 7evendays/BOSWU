import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyrebase
import json
from src.settings import *
from src.profileDialog import ProfileDialog
from src.movieSplashScreen import *
from src.loginDialog import LoginDialog
from src.signupDialog import SignUpDialog
from src.noticeDialog import NoticeDialog

# 전역 변수
img_path = "src/imgsource/"

with open("firebase/auth.json") as f:
            config = json.load(f)
firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
# Get a reference to the database service
db = firebase.database()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        settings.initialInfo()
        self.setupUI()

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(MainWindow, self).keyPressEvent(event)

    def setupUI(self):
        self.resize(560, 450)
        self.setWindowTitle("ChasEye 체이스아이 :: 메인")
        self.setWindowIcon(QIcon(img_path + "icon.png"))

        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        # label for header logo
        self.headerLable = QLabel()
        self.headerLable.setPixmap(QtGui.QPixmap(img_path + "logo.png"))

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
        self.signupLabel = QLabel("ChasEye에 처음이신가요?")
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
        self.headerLayout = QVBoxLayout()
        self.headerLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.profileBox = QVBoxLayout()
        self.btnBox = QVBoxLayout()
        self.btnBox.setContentsMargins(0, 15, 0, 15)
        self.btnBox.setSpacing(15)
        self.btnBox.setAlignment(Qt.AlignCenter)
        self.signupBox = QHBoxLayout()
        self.signupBox.setAlignment(Qt.AlignCenter)
        
        self.outline.addLayout(self.headerLayout)
        self.headerLayout.addWidget(self.headerLable)
        self.outline.addLayout(self.mainLayout)
        self.mainLayout.addLayout(self.profileBox)
        self.mainLayout.addLayout(self.btnBox)
        self.btnBox.addWidget(self.loginBtn)
        self.btnBox.addLayout(self.signupBox)
        self.signupBox.addWidget(self.signupLabel)
        self.signupBox.addWidget(self.signupBtn)

    def profileBtnClicked(self):
        self.close()
        dlg = ProfileDialog()
        dlg.exec_()

        item = QtWidgets.QTableWidgetItem(settings.email)
        self.profileTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem(settings.uname)
        self.profileTable.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem(settings.sid)
        self.profileTable.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem(settings.major)
        self.profileTable.setItem(3, 1, item)

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
            
            # create splashscreen
            movie = QMovie(img_path + "splash.gif") #지금은 임의로 블로하이 넣어놓음
            splash = MovieSplashScreen(movie)
            splash.show()

            start = time.time()
            while movie.state() == QMovie.Running and time.time() < start + 0.5:
                QApplication.processEvents()
        else:
            pass

        self.show()

    def updateUI(self):
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
        pixmap = QPixmap(img_path + "profile.png")
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

        # button for exam dialog
        self.goexamBtn = QPushButton("시험 시작")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.goexamBtn.setMinimumSize(100, 60)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.logoutBtn.setMinimumSize(100, 60)
        self.logoutBtn.setSizePolicy(sizePolicy)
        font.setPointSize(14)
        self.logoutBtn.setFont(font)
        self.logoutBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.logoutBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.logoutBtn.clicked.connect(self.logoutBtnClicked)
        
        # table for profile
        self.profileTable = QTableWidget()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(75)
        self.profileTable.setFont(font)
        self.profileTable.setRowCount(4)
        self.profileTable.setColumnCount(2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.profileTable.setMinimumSize(300, 200)
        self.profileTable.setMaximumHeight(300)
        self.profileTable.setSizePolicy(sizePolicy)
        self.profileTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # 수평 스크롤바
        self.profileTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # 수직 스크롤바
        self.profileTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # 수정 불가능
        self.profileTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection) # 선택 불가능
        self.profileTable.setShowGrid(False) # 그리드 해제
        self.profileTable.setCornerButtonEnabled(False) # 코너 버튼 불가능
        self.profileTable.horizontalHeader().setVisible(False) # 수평 머리말
        self.profileTable.verticalHeader().setVisible(False) # 수직 머리말
        self.profileTable.setStyleSheet("background-color : qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(7, 163, 183, 255), stop:1 rgba(218, 235, 199, 255));\n"
                                        "color : white;\n"
                                        "border-radius : 10px;\n"
                                        "padding : 10px;\n")
        header = self.profileTable.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
        # 1행
        item = QtWidgets.QTableWidgetItem("이메일")
        self.profileTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem("이름")
        self.profileTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem("학번")
        self.profileTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem("학과")
        self.profileTable.setItem(3, 0, item)
        # 2행
        item = QtWidgets.QTableWidgetItem(settings.email)
        self.profileTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem(settings.uname)
        self.profileTable.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem(settings.sid)
        self.profileTable.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem(settings.major)
        self.profileTable.setItem(3, 1, item)
        
        self.headerLayout.addWidget(self.profileBtn)
        self.profileBox.addWidget(self.profileTable)
        self.btnBox.addWidget(self.goexamBtn)
        self.btnBox.addWidget(self.logoutBtn)

    def logoutBtnClicked(self):
        settings.expireInfo()
        self.profileBtn.setParent(None)
        self.profileTable.setParent(None)
        self.goexamBtn.setParent(None)
        self.logoutBtn.setParent(None)
        
        self.btnBox.addWidget(self.loginBtn)
        self.btnBox.addLayout(self.signupBox)
        self.signupBox.addWidget(self.signupLabel)
        self.signupBox.addWidget(self.signupBtn)