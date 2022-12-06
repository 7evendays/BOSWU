from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyrebase
import json
from src.settings import *
from src.signupDialog import SignUpDialog

img_path = "src/imgsource/"

with open("firebase/auth.json") as f:
            config = json.load(f)
firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
# Get a reference to the database service
db = firebase.database()


class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        self.setupUI()

    def setupUI(self):
        self.setFixedSize(340, 280)
        self.setWindowTitle("ChasEye 체이스아이 :: 로그인")
        self.setWindowIcon(QIcon(img_path + "icon.png"))

        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")

        # label for header
        self.headerLabel = QLabel("로그인")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.headerLabel.setFixedHeight(40) # 높이 고정
        self.headerLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.headerLabel.setFont(font)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.headerLabel.setStyleSheet("color: #07A3B7;\n")

        # label for email
        self.emailLabel = QLabel("아이디")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.emailLabel.setFont(font)
        self.emailLabel.setStyleSheet("color: #07A3B7;\n")
        # text field for email
        self.emailInput = QLineEdit()
        self.emailInput.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9@.]+")))
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(75)
        self.emailInput.setFont(font)
        self.emailInput.setStyleSheet("border-radius : 10px;\n")

        # label for passwordBox
        self.passwordLabel = QLabel("비밀번호")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setStyleSheet("color: #07A3B7;\n")
        # text field for passwordBox
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(75)
        self.passwordInput.setFont(font)
        self.passwordInput.setStyleSheet("border-radius : 10px;\n")

        # button for login
        self.loginBtn = QPushButton("로그인")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.loginBtn.setFont(font)
        self.loginBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.loginBtn.setStyleSheet("background-color : #07A3B7;\n"
                                    "color : #FFF;\n"
                                    "border-radius : 10px;\n"
                                    "padding : 4px;\n")
        self.loginBtn.clicked.connect(self.loginBtnClicked)

        # label for error
        self.errorLabel = QLabel("")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.errorLabel.setFont(font)
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.errorLabel.setStyleSheet("color: #07A3B7;\n"
                                       "margin : 8px 0px 8px 0px;\n")

        # label for signupBox
        self.signupLabel = QLabel("ChasEye에 처음이신가요?")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.signupLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 확장
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
        self.outline.setSpacing(8)
        self.formLayout = QFormLayout()
        self.signupBox = QHBoxLayout()

        self.outline.addWidget(self.headerLabel)
        self.outline.addLayout(self.formLayout)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.emailLabel)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.emailInput)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordInput)
        self.outline.addWidget(self.loginBtn)
        self.outline.addWidget(self.errorLabel)
        self.outline.addLayout(self.signupBox)
        self.signupBox.addWidget(self.signupLabel)
        self.signupBox.addWidget(self.signupBtn)

    def loginBtnClicked(self):
        self.loginfunction()

    def signupBtnClicked(self):
        self.close()
        dlg = SignUpDialog()
        dlg.exec_()

    def loginfunction(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()
        
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(img_path + "alert.png"))
        msg.setWindowTitle("로그인")

        if len(email) == 0 or len(password) == 0:
            self.errorLabel.setText("공란이 있습니다.")
        else:
            try:
                # Log the user in
                settings.login = auth.sign_in_with_email_and_password(email, password)
                self.verified = auth.get_account_info(settings.login["idToken"])["users"][0]["emailVerified"]

                if self.verified != False:
                    self.errorLabel.setText("성공적으로 로그인했습니다.")
                    msg.setIconPixmap(QPixmap(img_path + "success.png").scaled(40, 40))
                    msg.setText("알림")
                    msg.setInformativeText("성공적으로 로그인했습니다.")
                    msg.exec_()
                    self.close()
                    
                    settings.setInfo()
                    self.errorLabel.clear()
                    self.emailInput.clear()
                    self.passwordInput.clear()
                else:
                    settings.login = False
                    self.errorLabel.setText("미인증 상태입니다.")
                    msg.setIconPixmap(QPixmap(img_path + "fail.png").scaled(40, 40))
                    msg.setText("알림")
                    msg.setInformativeText("이메일 인증을 진행해주세요.")
                    msg.exec_()
                    
                    self.emailInput.clear()
                    self.passwordInput.clear()
            except:
                self.errorLabel.setText("이메일 혹은 비밀번호를 잘못 입력하셨습니다.")
                self.emailInput.clear()
                self.passwordInput.clear()
    