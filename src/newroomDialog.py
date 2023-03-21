from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
from key_generator.key_generator import generate
from src.settings import *


class NewRoomDailog(QDialog):
    def __init__(self):
        super(NewRoomDailog, self).__init__()
        self.setupUI()
    
    def setupUI(self):
        self.resize(520, 420)
        self.setWindowTitle("BOSWU 보슈 :: 방 생성")
        self.setWindowIcon(QIcon(settings.img_path + "icon.png"))

        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

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

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        self.headerLabel = QLabel("방 생성")
        self.headerLabel.setMinimumWidth(80)
        self.headerLabel.setFixedHeight(40) # 높이 고정
        self.headerLabel.setSizePolicy(sizePolicy)
        self.headerLabel.setFont(largefont)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.headerLabel.setStyleSheet("color: #07A3B7;\n")
        
        self.nameLabel = QLabel("담당자")
        self.nameLabel.setMinimumWidth(80)
        self.nameLabel.setFixedHeight(40)
        self.nameLabel.setSizePolicy(sizePolicy)
        self.nameLabel.setFont(basicfont)
        self.nameLabel.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.nameLabel.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        self.nameField = QLabel(settings.db.child("users").child(settings.uid).child("name").get().val())
        self.nameField.setFont(basicfont)

        self.roomId = self.generatekey()
        self.roomidLabel = QLabel("방 ID")
        self.roomidLabel.setMinimumWidth(80)
        self.roomidLabel.setFixedHeight(40)
        self.roomidLabel.setSizePolicy(sizePolicy)
        self.roomidLabel.setFont(basicfont)
        self.roomidLabel.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.roomidLabel.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        self.roomidField = QLabel(self.roomId)
        self.roomidField.setFont(basicfont)

        self.subjectLabel = QLabel("과목명")
        self.subjectLabel.setMinimumWidth(80)
        self.subjectLabel.setFixedHeight(40)
        self.subjectLabel.setSizePolicy(sizePolicy) # 너비 고정 높이 고정
        self.subjectLabel.setFont(basicfont)
        self.subjectLabel.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.subjectLabel.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        self.subjectField = QComboBox()
        subjects = settings.db.child("majors").child("정보보호학과").child("subjects").get()
        for subject in subjects.each():
            self.subjectField.addItem(subject.val())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.subjectField.setFixedHeight(40) # 높이 고정
        self.subjectField.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        self.subjectField.setFont(basicfont)
        self.subjectField.setStyleSheet("border-radius : 10px;\n")

        self.classLabel = QLabel("분반")
        self.classLabel.setMinimumWidth(80)
        self.classLabel.setFixedHeight(40) # 높이 고정
        self.classLabel.setSizePolicy(sizePolicy)
        self.classLabel.setFont(basicfont)
        self.classLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.classLabel.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        self.classField = QSpinBox()
        self.classField.setFixedHeight(40)
        self.classField.setFont(basicfont)
        self.classField.setMinimum(1)
        self.classField.setMaximum(4)
        self.classField.setStyleSheet("border-radius : 10px;\n")

        self.dateLabel = QLabel("시험 일시")
        self.dateLabel.setMinimumWidth(80)
        self.dateLabel.setFixedHeight(40) # 높이 고정
        self.dateLabel.setSizePolicy(sizePolicy)
        self.dateLabel.setFont(basicfont)
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.dateLabel.setStyleSheet("background-color: #07A3B7;\n"
                                      "color: #FFF;\n"
                                      "padding : 8px\n")
        self.dateField = QDateEdit()
        self.dateField.setMinimumDate(datetime.datetime.now())
        self.dateField.setCalendarPopup(True)
        self.dateField.setStyleSheet("border-radius : 10px;\n")
        self.dateField.setFixedHeight(40)
        self.dateField.setFont(basicfont)
        self.timeField = QTimeEdit()
        self.timeField.setTime(QTime.currentTime())
        self.timeField.setStyleSheet("border-radius : 10px;\n")
        self.timeField.setFixedHeight(40)
        self.timeField.setFont(basicfont)
        
        self.createBtn = QPushButton("방 생성하기")
        medianfont.setBold(True)
        self.createBtn.setFont(medianfont)
        self.createBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.createBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.createBtn.clicked.connect(self.createBtnClicked)
        
        self.outline = QVBoxLayout(self)
        self.outline.setSpacing(8)
        self.formLayout = QFormLayout()

        self.outline.addWidget(self.headerLabel)
        self.outline.addLayout(self.formLayout)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameField)
        
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.roomidLabel)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.roomidField)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.subjectLabel)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.subjectField)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.classLabel)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.classField)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.dateLabel)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dateField)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.timeField)
        self.outline.addWidget(self.createBtn)
    

    def generatekey(self):
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seed = settings.uid + self.time
        self.roomId = generate(3, ' ', 4, 4, type_of_value = 'int', capital = 'none', seed = seed).get_key()
        cnt = 0

        while settings.db.child("rooms").child("current").child(self.roomId).get().val() != None:
            cnt += cnt
            self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            newseed = settings.uid + self.time
            self.roomId = generate(3, ' ', 4, 4, type_of_value = 'int', capital = 'none', seed = newseed).get_key()
            if cnt > 3:
                break
                
        return self.roomId
    
    def createBtnClicked(self):
        settings.db.child("rooms").child("current").child(settings.uid).child(self.roomId).set({
            "owner": settings.email,
            "create time": self.time,
            "subject": self.subjectField.currentText(),
            "class num": self.classField.value(),
            "test time": self.dateField.date().toString() + " " + self.timeField.time().toString()
        })

        msg = QMessageBox()
        msg.setWindowIcon(QIcon(settings.img_path + "alert.png"))
        msg.setWindowTitle("방 생성")
        msg.setIconPixmap(QPixmap(settings.img_path + "success.png").scaled(40, 40))
        msg.setText("알림")
        msg.setInformativeText("방이 생성되었습니다.")
        msg.exec_()

        self.close()