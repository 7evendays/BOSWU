from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyrebase
import json
from src.settings import *

img_path = "src/imgsource/"

with open("firebase/auth.json") as f:
            config = json.load(f)
firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
# Get a reference to the database service
db = firebase.database()


class ProfileDialog(QDialog):
    def __init__(self):
        super(ProfileDialog, self).__init__()
        self.setupUI()

    def setupUI(self):
        self.setFixedSize(340, 300)
        self.setWindowTitle("ChasEye 체이스아이 :: 프로필 설정")
        self.setWindowIcon(QIcon(img_path + "icon.png"))

        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")

        # label for header
        self.headerLabel = QLabel("프로필 수정")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.headerLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 확장
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.headerLabel.setFont(font)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.headerLabel.setStyleSheet("color: #07A3B7;\n")

        # label for email
        self.emailIndex = QLabel("아이디")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.emailIndex.setFixedWidth(90) # 너비 고정
        self.emailIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 고정
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.emailIndex.setFont(font)
        self.emailIndex.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.emailIndex.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        # label for email
        self.emailInput = QLineEdit(settings.email)
        self.emailInput.setReadOnly(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.emailInput.setFixedHeight(30) # 높이 고정
        self.emailInput.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.emailInput.setFont(font)
        self.emailInput.setStyleSheet("border-radius : 10px;\n")
        
        # label for name
        self.nameIndex = QLabel("이름")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.nameIndex.setFixedWidth(90) # 너비 고정
        self.nameIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 고정
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.nameIndex.setFont(font)
        self.nameIndex.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.nameIndex.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        # label for name
        self.nameInput = QLineEdit(settings.uname)
        self.nameInput.setValidator(QRegExpValidator(QRegExp("[가-힣]+"))) # 한글만 입력
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.nameInput.setFixedHeight(30) # 높이 고정
        self.nameInput.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.nameInput.setFont(font)
        self.nameInput.setStyleSheet("border-radius : 10px;\n")

        # label for sid
        self.sidIndex = QLabel("학번")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.sidIndex.setFixedWidth(90) # 너비 고정
        self.sidIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 확장
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.sidIndex.setFont(font)
        self.sidIndex.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.sidIndex.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        # line edit for sid
        self.sidInput = QLineEdit(settings.sid)
        self.sidInput.setValidator(QRegExpValidator(QRegExp("[0-9]{10}$"))) # 숫자만 입력 # 입력 10자리 제한
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.sidInput.setFixedHeight(30) # 높이 고정
        self.sidInput.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sidInput.setFont(font)
        self.sidInput.setStyleSheet("border-radius : 10px;\n")

        # label for major
        self.majorIndex = QLabel("학과")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.majorIndex.setFixedWidth(90) # 너비 고정
        self.majorIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 확장
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.majorIndex.setFont(font)
        self.majorIndex.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.majorIndex.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        # line edit for sid
        self.majorInput = QComboBox()
        majors = db.child("major").get()
        for major in majors.each():
            self.majorInput.addItem(major.val())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.majorInput.setFixedHeight(30) # 높이 고정
        self.majorInput.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(75)
        self.majorInput.setFont(font)
        self.majorInput.setStyleSheet("border-radius : 10px;\n")        
        self.majorInput.setCurrentText(settings.major)

        # button for edit
        self.editBtn = QPushButton("적용")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.editBtn.setFont(font)
        self.editBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.editBtn.setStyleSheet("background-color : #07A3B7;\n"
                                    "color : #FFF;\n"
                                    "border-radius : 10px;\n")
        self.editBtn.clicked.connect(self.editBtnClicked)

        self.outline = QVBoxLayout(self)
        self.profileLayout = QVBoxLayout()
        self.profileLayout.setAlignment(Qt.AlignLeft)
        self.profileLayout.setContentsMargins(0, 15, 0, 15)
        self.profileLayout.setSpacing(8)
        
        self.emailBox = QHBoxLayout()
        self.nameBox = QHBoxLayout()
        self.sidBox = QHBoxLayout()
        self.majorBox = QHBoxLayout()
        
        self.outline.addWidget(self.headerLabel)
        self.outline.addLayout(self.profileLayout)

        self.profileLayout.addLayout(self.emailBox)
        self.emailBox.addWidget(self.emailIndex)
        self.emailBox.addWidget(self.emailInput)
        
        self.profileLayout.addLayout(self.nameBox)
        self.nameBox.addWidget(self.nameIndex)
        self.nameBox.addWidget(self.nameInput)

        self.profileLayout.addLayout(self.sidBox)
        self.sidBox.addWidget(self.sidIndex)
        self.sidBox.addWidget(self.sidInput)

        self.profileLayout.addLayout(self.majorBox)
        self.majorBox.addWidget(self.majorIndex)
        self.majorBox.addWidget(self.majorInput)

        self.outline.addWidget(self.editBtn)

    def editBtnClicked(self):
        name = self.nameInput.text()
        sid = self.sidInput.text()
        major = self.majorInput.currentText()

        if name != "" and sid != "" and len(sid) == 10:
            settings.uname = name
            settings.sid = sid
            settings.major = major

            db.child("users").child(settings.uid).update({
                "name": settings.uname,
                "sid": settings.sid,
                "major": settings.major
            })
            self.close()
        else:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(img_path + "alert.png"))
            msg.setWindowTitle("프로필 수정")
            msg.setIconPixmap(QPixmap(img_path + "fail.png").scaled(40, 40))
            msg.setText("알림")
            msg.setInformativeText("양식을 확인해주세요.")
            msg.exec_()