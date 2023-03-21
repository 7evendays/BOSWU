from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.settings import *


class ProfileDialog(QDialog):
    def __init__(self):
        super(ProfileDialog, self).__init__()
        self.setupUI()

    def setupUI(self):
        if settings.admin == False:
            self.setFixedSize(340, 300)
        else:
            self.setFixedSize(340, 260)
        self.setWindowTitle("BOSWU 보슈 :: 프로필 설정")
        self.setWindowIcon(QIcon(settings.img_path + "icon.png"))

        # small font
        smallfont = QFont()
        smallfont.setPointSize(10)
        smallfont.setBold(False)
        smallfont.setWeight(75)

        # basic font
        basicfont = QFont()
        basicfont.setPointSize(12)
        basicfont.setBold(False)
        basicfont.setWeight(75)
        basicfont.setFamily("맑은 고딕")
        
        # median font
        medianfont = QFont()
        medianfont.setPointSize(14)
        medianfont.setBold(False)
        medianfont.setWeight(75)
        medianfont.setFamily("맑은 고딕")

        # large font
        largefont = QFont()
        largefont.setPointSize(18)
        largefont.setBold(True)
        largefont.setWeight(75)
        largefont.setFamily("맑은 고딕")

        # label for header
        self.headerLabel = QLabel("프로필 수정")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.headerLabel.setFixedHeight(30)
        self.headerLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 확장
        self.headerLabel.setFont(largefont)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.headerLabel.setStyleSheet("color: #07A3B7;\n")

        # label for email
        self.emailIndex = QLabel("아이디")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.emailIndex.setFixedWidth(90) # 너비 고정
        self.emailIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 고정
        self.emailIndex.setFont(medianfont)
        self.emailIndex.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.emailIndex.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        # label for email
        self.emailInput = QLabel(settings.email)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.emailInput.setFixedHeight(30) # 높이 고정
        self.emailInput.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        self.emailInput.setFont(basicfont)
        self.emailInput.setStyleSheet("color: #07A3B7;\n")
        
        # label for name
        self.nameIndex = QLabel("이름")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.nameIndex.setFixedWidth(90) # 너비 고정
        self.nameIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 고정
        self.nameIndex.setFont(medianfont)
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
        self.nameInput.setFont(basicfont)
        self.nameInput.setStyleSheet("border-radius : 10px;\n")

        # label for sid
        self.sidIndex = QLabel("학번")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.sidIndex.setFixedWidth(90) # 너비 고정
        self.sidIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 확장
        self.sidIndex.setFont(medianfont)
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
        self.sidInput.setFont(basicfont)
        self.sidInput.setStyleSheet("border-radius : 10px;\n")

        # label for major
        self.majorIndex = QLabel("학과")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.majorIndex.setFixedWidth(90) # 너비 고정
        self.majorIndex.setSizePolicy(sizePolicy) # 너비 고정 높이 확장
        self.majorIndex.setFont(medianfont)
        self.majorIndex.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.majorIndex.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        # line edit for sid
        self.majorInput = QComboBox()
        majors = settings.db.child("majors").get()
        for major in majors.each():
            self.majorInput.addItem(major.key())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.majorInput.setFixedHeight(30) # 높이 고정
        self.majorInput.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        self.majorInput.setFont(basicfont)
        self.majorInput.setStyleSheet("border-radius : 10px;\n")        
        self.majorInput.setCurrentText(settings.major)

        # button for edit
        self.editBtn = QPushButton("적용")
        self.editBtn.setFont(medianfont)
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

        if settings.admin == False:
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

        msg = QMessageBox()
        msg.setWindowIcon(QIcon(settings.img_path + "alert.png"))
        msg.setWindowTitle("프로필 수정")
        msg.setIconPixmap(QPixmap(settings.img_path + "fail.png").scaled(40, 40))
        msg.setText("알림")
        msg.setInformativeText("양식을 확인해주세요.")

        if settings.admin == False:
            if name != "" and sid != "" and len(sid) == 10:
                settings.uname = name
                settings.sid = sid
                settings.major = major

                settings.db.child("users").child(settings.uid).update({
                    "name": settings.uname,
                    "sid": settings.sid,
                    "major": settings.major
                })
                self.close()
            else:
                msg.exec_()
        else:
            if name != "":
                settings.uname = name
                settings.major = major

                settings.db.child("users").child(settings.uid).update({
                    "name": settings.uname,
                    "major": settings.major
                })
                self.close()
            else:
                msg.exec_()