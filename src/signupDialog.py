from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.settings import *


class SignUpDialog(QDialog):
    def __init__(self):
        super(SignUpDialog, self).__init__()
        self.setupUI()

    def closeEvent(self, event):
        if self.emailInput.text() != "" and self.passwordInput.text() != "":
            try:
                temp_login = settings.auth.sign_in_with_email_and_password(self.email, self.password)
                temp_verify = settings.auth.get_account_info(temp_login["idToken"])["users"][0]["emailVerified"]
                
                if temp_verify == False:
                    msg = QMessageBox()
                    msg.setWindowIcon(QIcon(settings.img_path + "alert.png"))
                    msg.setWindowTitle("회원가입")
                    msg.setIconPixmap(QPixmap(settings.img_path + "info.png").scaled(40, 40))
                    msg.setText("알림")
                    msg.setInformativeText("계정은 생성되었으나 미인증 상태입니다.\n로그인은 인증 후 가능합니다.\n인증을 진행해주세요.")
                    msg.exec_()
            except:
                print("error")

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(SignUpDialog, self).keyPressEvent(event)

    def setupUI(self):
        self.setFixedSize(340, 340)
        self.setWindowTitle("BOSWU 보슈 :: 회원가입")
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
        self.headerLabel = QLabel("회원가입")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.headerLabel.setFixedHeight(40) # 높이 고정
        self.headerLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        self.headerLabel.setFont(largefont)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.headerLabel.setStyleSheet("color: #07A3B7;\n")


        # form Layout Widget
        self.formLayout = QtWidgets.QFormLayout()

        # admin
        self.adminLabel = QLabel("권한")
        self.adminLabel.setFont(basicfont)
        self.adminLabel.setStyleSheet("color: #07A3B7;\n")
        self.adminRadio1 = QRadioButton("감독관")
        self.adminRadio1.setChecked(False)
        self.adminRadio2 = QRadioButton("학생")
        self.adminRadio2.setChecked(True)
        
        # label for email
        self.emailLabel = QLabel("이메일")
        self.emailLabel.setFont(basicfont)
        self.emailLabel.setStyleSheet("color: #07A3B7;\n")
        # line edit for email
        self.emailInput = QtWidgets.QLineEdit()
        self.emailInput.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9@.]+")))
        self.emailInput.setPlaceholderText("실제 사용하는 이메일을 적어주세요.")
        self.emailInput.setStyleSheet("border-radius : 10px;\n"
                                      "padding : 4px;")

        # label for password
        self.passwordLabel = QLabel("비밀번호")
        self.passwordLabel.setFont(basicfont)
        self.passwordLabel.setStyleSheet("color: #07A3B7;\n")
        # line edit for password
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setStyleSheet("border-radius : 10px;\n"
                                         "padding : 4px;")

        # label for confirm
        self.confirmLabel = QLabel("비밀번호 재확인")
        self.confirmLabel.setFont(basicfont)
        self.confirmLabel.setStyleSheet("color: #07A3B7;\n")
        # line edit for confirm
        self.confirmInput = QLineEdit()
        self.confirmInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmInput.setStyleSheet("border-radius : 10px;\n"
                                        "padding : 4px;")
        self.confirmInput.textChanged.connect(self.checkfuction)

        # button for verify
        self.verifyBtn = QPushButton("인증메일 받기")
        medianfont.setBold(True)
        self.verifyBtn.setFont(medianfont)
        self.verifyBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.verifyBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.verifyBtn.clicked.connect(self.verifyBtnClicked)
        # button for resend
        self.resendBtn = QPushButton("메일 재전송")
        self.resendBtn.setFont(medianfont)
        self.resendBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.resendBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.resendBtn.clicked.connect(self.resendBtnClicked)
        # button for check
        self.checkBtn = QPushButton("인증 확인")
        self.checkBtn.setFont(medianfont)
        self.checkBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.checkBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.checkBtn.clicked.connect(self.verifyCheckfunction)

        # label for name
        self.nameLabel = QLabel("이름")
        self.nameLabel.setFont(basicfont)
        self.nameLabel.setStyleSheet("color: #07A3B7;\n")
        # line edit for name
        self.nameInput = QLineEdit()
        self.nameInput.setValidator(QRegExpValidator(QRegExp("[가-힣]+"))) # 한글만 입력
        self.nameInput.setStyleSheet("border-radius : 10px;\n"
                                     "padding : 4px;")

        # label for sid
        self.sidLabel = QLabel("학번")
        self.sidLabel.setFont(basicfont)
        self.sidLabel.setStyleSheet("color: #07A3B7;\n")
        # line edit for sid
        self.sidInput = QLineEdit()
        self.sidInput.setValidator(QRegExpValidator(QRegExp("[0-9]{10}$"))) # 숫자만 입력 # 입력 10자리 제한
        self.sidInput.setText("")
        self.sidInput.setStyleSheet("border-radius : 10px;\n"
                                    "padding : 4px;")

        # label for major
        self.majorLabel = QLabel("학과")
        self.majorLabel.setFont(basicfont)
        self.majorLabel.setStyleSheet("color: #07A3B7;\n")
        # line edit for sid
        self.majorInput = QComboBox()
        self.majorInput.setFont(basicfont)
        majors = settings.db.child("majors").get()
        for major in majors.each():
            self.majorInput.addItem(major.key())
        self.majorInput.setStyleSheet("border-radius : 10px;\n"
                                      "padding : 4px;")

        # label for error
        self.errorLabel = QLabel("인증에 필요하니 실제 사용하는 이메일을 적어주세요.")
        self.errorLabel.setFont(smallfont)
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.errorLabel.setStyleSheet("color: #07A3B7;\n"
                                      "margin : 8px 0px 4px 0px;\n")        

        # button for signup
        self.signupBtn = QPushButton("회원가입 하기")
        self.signupBtn.setFont(medianfont)
        self.signupBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.signupBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n"
                                     "margin : 4px;\n")
        self.signupBtn.clicked.connect(self.signupBtnClicked)

        # set Layout
        self.outline = QVBoxLayout(self)
        self.adminLayout = QHBoxLayout()
        self.formLayout = QFormLayout()
        self.btnLayout = QHBoxLayout()

        self.outline.addWidget(self.headerLabel)
        
        self.outline.addLayout(self.formLayout)
        self.adminLayout.addWidget(self.adminRadio1)
        self.adminLayout.addWidget(self.adminRadio2)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.adminLabel)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.adminLayout)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.emailLabel)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.emailInput)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.passwordInput)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.confirmLabel)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.confirmInput)
        self.outline.addWidget(self.errorLabel)
        self.outline.addWidget(self.verifyBtn)
    
    def verifyBtnClicked(self):
        self.verifyfunction()

    def resendBtnClicked(self):
        self.resendfunction()

    def nextBtnClicked(self):
        self.nextfunction()

    def signupBtnClicked(self):
        self.signupfunction()

    def checkfuction(self):
        password = self.passwordInput.text()
        confirm = self.confirmInput.text()
        
        if password != confirm:
            self.confirmInput.setStyleSheet("background-color : #07A3B7;\n"
                                            "color : #FFF;\n"
                                            "border : #DAEBC7;\n"
                                            "border-radius : 10px;\n"
                                            "padding : 4px;")
        else:
            self.confirmInput.setStyleSheet("border-radius : 10px;\n"
                                            "padding : 4px;")
    
    def verifyfunction(self):
        self.email = self.emailInput.text()
        self.password = self.passwordInput.text()
        self.confirm = self.confirmInput.text()
        self.admin = self.adminRadio1.isChecked()
        
        if len(self.email) == 0 or len(self.password) == 0 or len(self.confirm) == 0:
            self.errorLabel.setText("이메일과 비밀번호를 모두 입력해주세요.")
        elif self.password != self.confirm:
            self.errorLabel.setText("비밀번호가 일치하지 않습니다.")
        else:
            try:
                self.new = settings.auth.create_user_with_email_and_password(self.email, self.password)
                data = {
                    "email": self.new["email"],
                    "login": False
                }

                settings.db.child("users").child(self.new["localId"]).set(data) # db에 추가

                # before the 1 hour expiry:
                settings.auth.refresh(self.new["refreshToken"])
                # now we have a fresh token
                settings.auth.send_email_verification(self.new["idToken"])
                print(self.new)
                self.errorLabel.setText("이메일을 발송했습니다. 인증을 진행해주세요.")
                
                self.adminRadio1.setDisabled(True)
                self.adminRadio2.setDisabled(True)
                self.emailInput.setDisabled(True)
                self.passwordInput.setDisabled(True)
                self.confirmInput.setDisabled(True)
                self.verifyBtn.setParent(None)
                self.outline.addLayout(self.btnLayout)
                self.btnLayout.addWidget(self.resendBtn)
                self.btnLayout.addWidget(self.checkBtn)
            except:
                self.errorLabel.setText("이미 존재하는 아이디이거나, 너무 약한 비밀번호입니다.")
                self.emailInput.clear()
                self.passwordInput.clear()
                self.confirmInput.clear()

    def verifyCheckfunction(self):
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(settings.img_path + "alert.png"))
        msg.setWindowTitle("회원가입")

        try:
            # check verify
            self.verified = settings.auth.get_account_info(self.new["idToken"])["users"][0]["emailVerified"]

            if self.verified != False:
                self.errorLabel.setText("성공적으로 인증했습니다.")
                msg.setIconPixmap(QPixmap(settings.img_path + "success.png").scaled(40, 40))
                msg.setText("알림")
                self.resendBtn.setParent(None)
                msg.setInformativeText("성공적으로 인증했습니다.")
                msg.exec_()
                self.nextfunction()
            else:
                self.errorLabel.setText("미인증 상태입니다.")
                msg.setIconPixmap(QPixmap(settings.img_path + "fail.png").scaled(40, 40))
                msg.setText("알림")
                msg.setInformativeText("이메일 인증을 진행해주세요.\n※ 인증 이메일이 확인되지 않으면 스팸함을 확인해주세요.")
                msg.exec_()
        except:
            self.errorLabel.setText("인증에 실패했습니다.")
            self.close()

    def resendfunction(self):
        try:
            print(self.new)
            settings.auth.send_email_verification(self.new["idToken"])
            print(self.new)
            
            self.errorLabel.setText("이메일을 재발송했습니다. 인증을 진행해주세요.")
        except:
            self.errorLabel.setText("시간이 1분 이상 지난 후 다시 시도해주세요.")

    def nextfunction(self):
        self.adminLabel.setParent(None)
        self.adminLayout.setParent(None)
        self.adminRadio1.setParent(None)
        self.adminRadio2.setParent(None)
        self.emailLabel.setParent(None)
        self.emailInput.setParent(None)
        self.passwordLabel.setParent(None)
        self.passwordInput.setParent(None)
        self.confirmLabel.setParent(None)
        self.confirmInput.setParent(None)
        self.btnLayout.setParent(None)
        self.checkBtn.setParent(None)


        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameInput)
        

        if self.admin == True:
            self.setFixedSize(340, 240)
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.majorLabel)
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.majorInput)
        else:
            self.setFixedSize(340, 280)
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sidLabel)
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sidInput)
            self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.majorLabel)
            self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.majorInput)
            
        self.errorLabel.setText("")
        self.outline.addWidget(self.signupBtn)

    def signupfunction(self):
        name = self.nameInput.text()
        sid = self.sidInput.text()
        major = self.majorInput.currentText()
        data = None

        msg = QMessageBox()
        msg.setWindowIcon(QIcon(settings.img_path + "alert.png"))
        msg.setWindowTitle("회원가입")

        if self.admin == True:
            if name != "":
                data = {
                    "admin": self.admin,
                    "name": name,
                    "major": major
                }
            else:
                self.errorLabel.setText("양식을 다시 확인해주세요.")
        else:
            if name != "" and sid != "" and len(sid) == 10:
                data = {
                    "admin": self.admin,
                    "name": name,
                    "sid": sid,
                    "major": major,
                    "ip": settings.ip,
                    "eys": {
                        "r_std": settings.r_std,
                        "l_std": settings.l_std,
                        "d_std": settings.d_std
                    }
                }
            else:
                self.errorLabel.setText("양식을 다시 확인해주세요.")

        if data != None:
            settings.db.child("users").child(self.new["localId"]).update(data) # db에 추가

            msg.setIconPixmap(QPixmap(settings.img_path + "success.png").scaled(40, 40))
            msg.setText("알림")
            msg.setInformativeText("회원가입이 완료됐습니다.")
            msg.exec_()
            self.close()