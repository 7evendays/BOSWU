from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.examDialog import ExamDialog

img_path = "src/imgsource/"


class NoticeDialog(QDialog):
    def __init__(self):
        super(NoticeDialog, self).__init__()
        self.setupUI()

    def setupUI(self):
        self.resize(680, 420)
        self.setWindowTitle("ChasEye 체이스아이 :: 공지사항")
        self.setWindowIcon(QIcon(img_path + "icon.png"))

        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        
        # button for start exam
        self.startBtn = QPushButton("확인")
        font.setPointSize(14)
        font.setBold(True)
        self.startBtn.setFont(font)
        self.startBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.startBtn.setStyleSheet("background-color : #07A3B7;\n"
                                    "color : #FFF;\n"
                                    "border-radius : 10px;\n")
        self.startBtn.clicked.connect(self.startBtnClicked)
        
        # label for notice
        self.header = QtWidgets.QLabel("유의 사항\n")
        font.setPointSize(14)
        font.setBold(True)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setStyleSheet("color : #07A3B7;")

        self.lable1 = QtWidgets.QLabel("개인마다 캠의 위치가 다르니 최대한 캠의 각도가 정면을 바라볼 수 있도록 하고, "
                                       "캠에 얼굴이 정확하게 나올 수 있도록 조정해주세요.\n"
                                       "* 캠이 빛의 영향을 받을 수 있으니 "
                                       "응시자 시험 환경 설정에 주의해주시기 바랍니다.\n"
                                       "감시 프로그램과 시험 응시 탭 외에는 종료해주세요.\n"
                                       "\n부정행위로 의심될 경우 응시자의 캠 화면이 녹화되며 "
                                       "부정행위 기록 목적 외에는 사용하지 않습니다.\n"
                                       "기록은 시험 종료 한달 후 폐기됩니다.\n"
                                       "\n부정행위 기준은 다음과 같습니다.")
        font.setPointSize(12)
        font.setBold(False)
        self.lable1.setFont(font)
        self.lable1.setAlignment(QtCore.Qt.AlignCenter)
        self.lable1.setWordWrap(True)
        
        self.lable2 = QtWidgets.QLabel("1. 노트북 화면이 아닌 다른 곳을 약 5초간 바라볼 경우\n" 
                                       "2. 두 명 이상의 사람이 캠 화면에 잡힌 경우\n"
                                       "3. 응시자가 자리를 비운 경우\n"
                                       "4. 시험 응시 사이트 이외에 다른 사이트를 접속한 경우\n")
        font.setPointSize(12)
        font.setBold(False)
        self.lable2.setFont(font)
        self.lable2.setAlignment(QtCore.Qt.AlignCenter)
        self.lable2.setWordWrap(True)
        self.lable2.setStyleSheet("color : #07A3B7;")
        
        outline = QVBoxLayout(self)
        outline.setContentsMargins(30, 30, 30, 30)

        outline.addWidget(self.header)
        outline.addWidget(self.lable1)
        outline.addWidget(self.lable2)
        outline.addWidget(self.startBtn, alignment = Qt.AlignCenter)
        
    def startBtnClicked(self):
        self.close()
        dlg = ExamDialog()
        dlg.exec_()