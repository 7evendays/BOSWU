import cv2, qimage2ndarray
import mediapipe as mp
import statistics
from scapy.all import *
from PIL import ImageGrab
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from src.settings import *
from src.detection import *

webcam = None
camera = None
global log_list
log_list = []
ri_cnt = 0
le_cnt = 0
dw_cnt = 0
alert_cnt = 0
alert_le = 0
alert_ri = 0
alert_dw = 0
alert_emp = 0
alert_two = 0
alert_int = 0
yellowcard = 0
protocols = {1: 'ICMP', 6: 'TCP', 17:'UDP'}
global pre_time, pkt_cnt, cap, approv, chk, ip_list
pre_time = datetime.now()
pkt_cnt = 0
lock = threading.Lock()
approv = False
cap = False
chk = 0
ip_list = set()
HOST = socket.gethostbyname(socket.gethostname())


class CamtestDialog(QDialog):
    def __init__(self):
        super(CamtestDialog, self).__init__()
        self.setupUI()
        
    def closeEvent(self, event):
        self.endWebcam()

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(CamtestDialog, self).keyPressEvent(event)
        
    def setupUI(self):
        self.resize(720, 480)
        self.setWindowTitle("BOSWU 보슈 :: 카메라 테스트")
        self.setWindowIcon(QIcon(settings.img_path + "icon.png"))
        
        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")

        # label for header
        self.headerLabel = QLabel("카메라 테스트")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.headerLabel.setMaximumHeight(60) # 최대 높이
        self.headerLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 확장
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.headerLabel.setFont(font)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.headerLabel.setStyleSheet("background-color: #07A3B7;\n"
                                       "color: #FFF;\n"
                                       "border-radius: 10px;\n"
                                       "padding: 8px;")
        
        # label for alert title
        self.alertTitleLabel = QLabel("경고 기록")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.alertTitleLabel.setMaximumWidth(480) # 최대 너비
        self.alertTitleLabel.setFixedHeight(30) # 높이 고정
        self.alertTitleLabel.setSizePolicy(sizePolicy)
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.alertTitleLabel.setFont(font)
        self.alertTitleLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.alertTitleLabel.setStyleSheet("background-color: #07A3B7;\n"
                                           "color: #FFF;\n"
                                           "border-radius: 10px;\n")
        
        # widget for alert list
        self.alertListWidget = QListWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.alertListWidget.setMinimumWidth(280) # 최소 너비
        self.alertListWidget.setMaximumWidth(480) # 최대 너비
        self.alertListWidget.setSizePolicy(sizePolicy)
        font.setPointSize(10)
        font.setBold(False)
        self.alertListWidget.setFont(font)
        self.alertListWidget.setStyleSheet("border-radius: 10px;\n"
                                           "margin: 1px 1px 1px 1px;")
        self.alertListWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.alertListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # 횡스크롤바 없애기
        self.alertListWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.alertListWidget.setWordWrap(True) # 줄 넘기기
                
        # label for camera
        self.camLabel = QLabel()
        self.camLabel.setStyleSheet("margin: 10px 10px 10px 10px;")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.camLabel.setMinimumSize(QtCore.QSize(640, 480)) # 최소 사이즈(너비, 높이)
        self.camLabel.setSizePolicy(sizePolicy)
        self.camLabel.setPixmap(QtGui.QPixmap(settings.img_path + "cam.png"))
        self.camLabel.setScaledContents(True) # 이미지 크기 조정

        # button size policy
        btnsizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed) # 너비 확장 높이 고정   
        # button font policy
        btnfont = QtGui.QFont()
        btnfont.setFamily("맑은 고딕")
        btnfont.setPointSize(14)
        btnfont.setBold(True)
        btnfont.setWeight(75)

        # label for calibration
        self.caliLabel = QLabel("탐지가 정확하지 않나요? 교정을 시작하세요. 👉")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.caliLabel.setMaximumWidth(360) #최대 너비
        self.caliLabel.setFixedHeight(30) # 높이 고정
        self.caliLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(75)
        self.caliLabel.setFont(font)
        self.caliLabel.setAlignment(QtCore.Qt.AlignRight) # 오른쪽 정렬
        # button for calibration
        self.caliBtn = QPushButton("교정")
        self.caliBtn.setFixedWidth(120) # 너비 고정
        self.caliBtn.setFixedHeight(30) # 높이 고정
        self.caliBtn.setFont(btnfont)
        self.caliBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.caliBtn.setStyleSheet(#"background-color : #DAEBC7;\n"
                                     "color : #07A3B7;\n"
                                     "border : 2px solid #07A3B7;\n"
                                     "border-radius : 10px;\n"
                                     "padding: 4px;\n")
        self.caliBtn.clicked.connect(self.caliBtnClicked)
        # label for calibration initialize
        self.caliinitLabel = QLabel("교정된 설정에서 초기 설정으로 바꾸고 싶나요? 👉")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.caliinitLabel.setMaximumWidth(360) #최대 너비
        self.caliinitLabel.setFixedHeight(30) # 높이 고정
        self.caliinitLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(75)
        self.caliinitLabel.setFont(font)
        self.caliinitLabel.setAlignment(QtCore.Qt.AlignRight) # 오른쪽 정렬
        # button for calibration initialize
        self.caliinitBtn = QPushButton("초기화")
        self.caliinitBtn.setFixedWidth(120) # 너비 고정
        self.caliinitBtn.setFixedHeight(30) # 높이 고정
        self.caliinitBtn.setFont(btnfont)
        self.caliinitBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.caliinitBtn.setStyleSheet(#"background-color : #DAEBC7;\n"
                                     "color : #07A3B7;\n"
                                     "border : 2px solid #07A3B7;\n"
                                     "border-radius : 10px;\n"
                                     "padding: 4px;\n")
        self.caliinitBtn.clicked.connect(self.caliinitBtnClicked)
        
        # button for turn on camera
        self.camonBtn = QPushButton("카메라 켜기")
        self.camonBtn.setMaximumWidth(180) # 최대 너비
        self.camonBtn.setFixedHeight(30) # 높이 고정
        self.camonBtn.setSizePolicy(btnsizePolicy)
        self.camonBtn.setFont(btnfont)
        self.camonBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.camonBtn.setStyleSheet("background-color : #07A3B7;\n"
                                    "color : #FFF;\n"
                                    "border-radius : 10px;\n"
                                    "padding: 4px;\n")
        self.camonBtn.clicked.connect(self.camonBtnClicked)
        
        # button for turn off camera
        self.camoffBtn = QPushButton("카메라 끄기")
        self.camoffBtn.setMaximumWidth(180) # 최대 너비
        self.camoffBtn.setFixedHeight(30) # 높이 고정
        self.camoffBtn.setSizePolicy(btnsizePolicy)
        self.camoffBtn.setFont(btnfont)
        self.camoffBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.camoffBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.camoffBtn.clicked.connect(self.camoffBtnClicked)

        # button for go back
        self.gobackBtn = QPushButton("뒤로 가기")
        self.gobackBtn.setFixedWidth(120) # 너비 고정
        self.gobackBtn.setFixedHeight(30) # 높이 고정
        self.gobackBtn.setFont(btnfont)
        self.gobackBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.gobackBtn.setStyleSheet(#"background-color : #DAEBC7;\n"
                                     "color : #07A3B7;\n"
                                     "border : 2px solid #07A3B7;\n"
                                     "border-radius : 10px;\n"
                                     "padding: 4px;\n")
        self.gobackBtn.clicked.connect(self.gobackBtnClicked)

        outerLayout = QVBoxLayout(self)
        outerLayout.setContentsMargins(8, 8, 8, 8)
        outerLayout.setSpacing(8)
        innerLayout = QHBoxLayout()
        innerLayout.setSpacing(4)
        innerRightLayout = QVBoxLayout()
        alertLayout = QVBoxLayout()
        alertLayout.setContentsMargins(0, 0, 0, 8)
        alertLayout.setSpacing(4)
        caliLayout = QHBoxLayout()
        caliinitLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        
        outerLayout.addWidget(self.headerLabel)
        outerLayout.addLayout(innerLayout)
        innerLayout.addWidget(self.camLabel)
        innerLayout.addLayout(innerRightLayout)
        innerRightLayout.addLayout(alertLayout)
        innerRightLayout.addLayout(caliLayout)
        innerRightLayout.addLayout(caliinitLayout)
        innerRightLayout.addLayout(buttonLayout)
        alertLayout.addWidget(self.alertTitleLabel)
        alertLayout.addWidget(self.alertListWidget)
        caliLayout.addWidget(self.caliLabel)
        caliLayout.addWidget(self.caliBtn)
        caliinitLayout.addWidget(self.caliinitLabel)
        caliinitLayout.addWidget(self.caliinitBtn)
        buttonLayout.addWidget(self.camonBtn)
        buttonLayout.addWidget(self.camoffBtn)
        buttonLayout.addWidget(self.gobackBtn)

    def caliBtnClicked(self):
        if webcam != None and webcam.isOpened:
            pass
        else:
            self.startWebcam(1)

    def caliinitBtnClicked(self):
        settings.updatecali(0.46, 0.64, 0.74)

    def camonBtnClicked(self):
        if webcam != None and webcam.isOpened():
            pass
        else:
            self.startWebcam(0)

    def camoffBtnClicked(self):
        self.endWebcam()

    def gobackBtnClicked(self):
        if not (webcam == None):
            webcam.release()
        self.alertListWidget.clear()
        self.close()

    def startWebcam(self, mode):
        global start_time
        start_time = datetime.now()

        global webcam, ret, frame
        webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 0번 카메라 장치 연결
        #webcam.set(cv2.CAP_PROP_FPS, 10) # 프레임 수를 낮추고 싶으면 주석 해제
        ret, frame = webcam.read()
        
        e_alert_time = datetime.now() - timedelta(hours=1)
        t_alert_time = datetime.now() - timedelta(hours=1)
        global msg
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(settings.img_path + "alert.png"))
        msg.setWindowTitle("알림")
        reply = QMessageBox()
        reply.setWindowIcon(QIcon(settings.img_path + "alert.png"))
        reply.setWindowTitle("알림")
        yesBtn = reply.addButton("예", QMessageBox.AcceptRole)
        noBtn = reply.addButton("아니오", QMessageBox.RejectRole)
        reply.setDefaultButton(noBtn)

        self.stream = settings.db.child("users").stream(self.stream_handler)
        
        switch = 0
        h_list = []
        v_list = []
        try:
            while webcam.isOpened():
                # We get a new frame from the webcam
                ret, frame = webcam.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1) # 좌우반전
                # 성능을 향상시키려면 이미지를 작성 여부를 False으로 설정
                # 영상에 얼굴 감지 주석 그리기 기본값 : True
                frame.flags.writeable = True

                # 만약 카메라가 연결되어 있지 않으면 while 반복문 종료
                if not ret:
                    msg.setIconPixmap(QPixmap(settings.img_path + "info.png").scaled(40, 40))
                    msg.setText("오류")
                    msg.setInformativeText("웹캠을 찾을 수 없습니다.")
                    msg.exec_()
                    self.endWebcam()
                    break
                
                if mode == 0:
                    try:
                        global alert_emp, alert_two
                        face = facedetection(frame)
                        if face == 2:
                            if ((datetime.now() - t_alert_time).seconds) > 10:
                                #self.save_img() # 이미지 저장을 원하면 주석 해제
                                self.save_mp4(0) # 동영상 저장을 원하면 주석 해제
                                alert_two += 0.4
                                log_msg = "외부인이 감지됐습니다."
                                time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
                                log_list.append(time + " " +log_msg)
                                self.alertListWidget.addItem(time + " " + log_msg)
                                self.alertListWidget.scrollToBottom()
                                self.alert_show()
                            t_alert_time = datetime.now()
                        elif face == 0:
                            if ((datetime.now() - e_alert_time).seconds) > 10:
                                #self.save_img() # 이미지 저장을 원하면 주석 해제
                                self.save_mp4(0) # 동영상 저장을 원하면 주석 해제
                                alert_emp += 0.4
                                log_msg = "자리를 비우지 마세요."
                                time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
                                log_list.append(time + " " +log_msg)
                                self.alertListWidget.addItem(time + " " +log_msg)
                                self.alertListWidget.scrollToBottom()
                                self.alert_show()
                            e_alert_time = datetime.now()

                        global ri_cnt, le_cnt, dw_cnt
                        hdir, vdir = eyetracking(frame)
                        if vdir != "blink":
                            if hdir == "right":
                                le_cnt = 0
                                ri_temp = ri_cnt
                                ri_temp += 1
                                ri_cnt = ri_temp
                                self.cntalert()
                            elif hdir == "left":
                                ri_cnt = 0
                                dw_cnt = 0
                                le_temp = le_cnt
                                le_temp += 1
                                le_cnt = le_temp
                                self.cntalert()
                            elif hdir == "center":
                                ri_cnt = 0
                                le_cnt = 0
                                if vdir == "down":
                                    dw_temp = dw_cnt
                                    dw_temp += 1
                                    dw_cnt = dw_temp
                                    self.cntalert()
                                elif vdir == "center":
                                    dw_cnt = 0
                        else:
                            dw_cnt = 0
                    except:
                        self.endWebcam()
                        break
                elif mode == 1:
                    if facedetection(frame) == 0:
                        self.endWebcam()
                        msg.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
                        msg.setText("교정")
                        msg.setInformativeText("얼굴이 감지되지 않습니다. 카메라를 확인해주세요.")
                        msg.exec_()
                        break
                    if switch == 0:
                        msg.setIconPixmap(QPixmap(settings.img_path + "info.png").scaled(40, 40))
                        msg.setText("교정")
                        msg.setInformativeText("지금부터 교정을 시작합니다. 반드시 카메라는 정면에 위치시키고 안내에 따라 교정을 마쳐주세요.\n"
                                                "고개는 정면으로 향한 채로 오른쪽을 3초 간 응시해주세요.")
                        msg.exec_()
                        cali_start = datetime.now()
                        switch = 1
                    if datetime.now() < cali_start + timedelta(seconds=3):
                        h_ratio, v_ratio = calibration(frame)
                        h_list.append(h_ratio)
                    else:
                        #hr_ratio = statistics.median(h_list) # 중앙값
                        #print(f"median hr_ratio: {h_ratio: .2f}")
                        hr_ratio = statistics.mean(h_list)
                        print(f"mean hr_ratio: {hr_ratio: .2f}")
                        
                        if hr_ratio > 0.5 or hr_ratio < 0.35:
                            reply.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
                            reply.setText("교정")
                            reply.setInformativeText("평균적인 수치에서 벗어나 있습니다. "
                                    "잘못된 설정으로 인해 불이익이 생길 수 있습니다.\n"
                                    "이대로 설정하시겠습니까?")
                            reply.exec_()
                            if reply.clickedButton() == yesBtn:
                                mode = 2
                            elif reply.clickedButton() == noBtn:
                                mode = 1
                        else:
                            mode = 2
                        
                        switch = 0
                        h_list.clear()
                elif mode == 2:
                    if switch == 0:
                        msg.setIconPixmap(QPixmap(settings.img_path + "info.png").scaled(40, 40))
                        msg.setText("교정")
                        msg.setInformativeText("고개는 정면으로 향한 채로 왼쪽을 3초 간 응시해주세요.")
                        msg.exec_()
                        cali_start = datetime.now()
                        switch = 1
                    if datetime.now() < cali_start + timedelta(seconds=3):
                        h_ratio, v_ratio = calibration(frame)
                        h_list.append(h_ratio)
                    else:
                        #hl_ratio = statistics.median(h_list) # 중앙값
                        #print(f"median hl_ratio: {hl_ratio: .2f}")
                        hl_ratio = statistics.mean(h_list) # 평균값
                        print(f"mean hl_ratio: {hl_ratio: .2f}")

                        if hl_ratio > 0.7 or hl_ratio < 0.6:
                            reply.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
                            reply.setText("교정")
                            reply.setInformativeText("평균적인 수치에서 벗어나 있습니다. "
                                    "잘못된 설정으로 인해 불이익이 생길 수 있습니다.\n"
                                    "이대로 설정하시겠습니까?")
                            reply.exec_()
                            if reply.clickedButton() == yesBtn:
                                mode = 3
                            elif reply.clickedButton() == noBtn:
                                mode = 2
                        else:
                            mode = 3
                        
                        h_list.clear()
                        switch = 0
                elif mode == 3:
                    if switch == 0:
                        msg.setIconPixmap(QPixmap(settings.img_path + "info.png").scaled(40, 40))
                        msg.setText("교정")
                        msg.setInformativeText("고개는 정면으로 향한 채로 아래쪽을 3초 간 응시해주세요.")
                        msg.exec_()
                        cali_start = datetime.now()
                        switch = 1
                    if datetime.now() < cali_start + timedelta(seconds=3):
                        h_ratio, v_ratio = calibration(frame)
                        v_list.append(v_ratio)
                    else:
                        #d_ratio = statistics.median(v_list) # 중앙값
                        #print(f"median v_ratio: {d_ratio: .2f}")
                        d_ratio = statistics.mean(v_list) # 평균값
                        print(f"mean v_ratio: {d_ratio: .2f}")
                        
                        if d_ratio > 1:
                            self.endWebcam()
                            msg.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
                            msg.setText("교정")
                            msg.setInformativeText("신뢰도가 없는 입력값이 있습니다. 다시 측정해주세요.")
                            msg.exec_()
                            break
                        else:
                            if d_ratio > 0.9 or d_ratio < 0.65:
                                reply.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
                                reply.setText("교정")
                                reply.setInformativeText("평균적인 수치에서 벗어나 있습니다. "
                                        "잘못된 설정으로 인해 불이익이 생길 수 있습니다.\n"
                                        "이대로 설정하시겠습니까?")
                                reply.exec_()
                                if reply.clickedButton() == yesBtn:
                                    mode = 4
                                elif reply.clickedButton() == noBtn:
                                    mode = 3
                            else:
                                mode = 4

                        v_list.clear()
                        switch = 0
                elif mode == 4:
                    if abs(hl_ratio - hr_ratio) < 0.15 or abs(hl_ratio - hr_ratio) > 0.4:
                        msg.setIconPixmap(QPixmap(settings.img_path + "fail.png").scaled(40, 40))
                        msg.setText("교정")
                        msg.setInformativeText("측정값의 신뢰도가 의심되어 값이 적용되지 않습니다.")
                        msg.exec_()
                    else:
                        settings.updatecali(hr_ratio, hl_ratio, d_ratio)
                        self.endWebcam()
                        msg.setIconPixmap(QPixmap(settings.img_path + "success.png").scaled(40, 40))
                        msg.setText("교정")
                        msg.setInformativeText("교정이 끝났습니다. 반드시 탐지가 제대로 이루어지는지 재확인 후 시험을 응시해주세요.")
                        msg.exec_()
                        
                    self.endWebcam()
                    break
                
                image = qimage2ndarray.array2qimage(frame)
                self.camLabel.setPixmap(QPixmap(image))
                self.camLabel.setScaledContents(True) # 레이블이 사용 가능한 모든 공간을 채우기 위해 내용의 크기를 조정할지를 설정
                
                """
                global cap, alert_int, lock

                lock.acquire()
                threading.Thread(target = self.pktcap).start()
                lock.release()
                threading.Thread(target = self.chkcnt).start()

                if cap == True:
                    cap_time = datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")
                    img = ImageGrab.grab()
                    filename = "capture/screenshot/screenshot_{}.png".format(cap_time)
                    img.save(filename)
                    alert_int += 0.2
                    log_msg = "인터넷 활동이 감지됐습니다."
                    time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
                    log_list.append(time + " " +log_msg)
                    self.alertListWidget.addItem(time + " " + log_msg)
                    self.alertListWidget.scrollToBottom()
                    self.alert_show()
                    cap = False
                """
                if cv2.waitKey(10) == ord('q'):
                    self.endWebcam()
                    break
        except:
            self.endWebcam()
            print("Exiting")

    def stream_handler(self, message):
        # We only care if something changed
        if message["event"] in ("put", "patch"):
            print("Something changed")
            self.chkgrouptest()

    def chkgrouptest(self):
        host_ip = settings.ip
        ip_list = []
        
        all_users = settings.db.child("users").get()
        for user in all_users.each():
            uid = user.key()
            if uid != settings.uid:
                login = settings.db.child("users").child(uid).child("login").get().val()
                if login == True:
                    ip_list.append(settings.db.child("users").child(uid).child("ip").get().val())
        print(ip_list)
        
        cnt_ip = ip_list.count(host_ip)
        if cnt_ip > 0:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(settings.img_path + "alert.png"))
            msg.setWindowTitle("알림")
            msg.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
            msg.setText("경고")
            msg.setInformativeText("유사한 장소에 타응시생이 있음이 감지되어 감독관에게 알림이 갔습니다.\n"
                                   "지금부터 카메라를 이용하여 주변을 360도 각도로 촬영하여 사람이 없음을 녹화해주세요.\n"
                                   "OK 버튼을 누르면 자동으로 10초간 녹화가 진행됩니다.\n"
                                   "※ 녹화를 하지 않을 시 추후에 불이익이 발생할 수 있습니다.")
            msg.exec_()
            self.save_mp4(1)
            msg.setIconPixmap(QPixmap(settings.img_path + "success.png").scaled(40, 40))
            msg.setText("알림")
            msg.setInformativeText("녹화가 완료되었습니다.")
            msg.exec_()
            log_msg = "유사한 장소에 타응시생이 있음이 감지되어 감독관에게 알림이 갔습니다."
            time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            log_list.append([time, log_msg])
            self.alertListWidget.addItem(time + " " + log_msg) # 기록 추가
            self.alertListWidget.scrollToBottom()

    def pktcap(self):
        sniff(filter = "ip", prn = self.cntpacket, count = 5)

    def cntpacket(self, packet):
        global pkt_cnt, pre_time, approv, HOST, ip_list
        src_ip = packet[0][1].src
        dst_ip = packet[0][1].dst
        proto = packet[0][1].proto
        
        l_host_ip = HOST.split(".")
        del(l_host_ip[3])
        s_host_ip = ".".join(l_host_ip)
        
        l_src_ip = src_ip.split(".")
        del(l_src_ip[3])
        s_src_ip = ".".join(l_src_ip)

        l_dst_ip = dst_ip.split(".")
        del(l_dst_ip[3])
        s_dst_ip = ".".join(l_dst_ip)

        if proto in protocols:
            if (s_src_ip == s_host_ip and s_dst_ip == s_host_ip) is not True:
                if int(l_src_ip[0]) > 127 and int(l_dst_ip[0]) > 127:
                    if src_ip == "203.246.40.30" or dst_ip == "203.246.40.30":
                        approv = True
                    else:
                        pkt_cnt += 1
                        ip_list.add(src_ip)
                        approv = False

    def chkcnt(self):
        global pkt_cnt, pre_time, cap, approv, chk
        time = datetime.now()

        if (time - pre_time).seconds >= 1.5:
            print(pkt_cnt)
            
            if approv == True:
                approv = False
            else:
                if pkt_cnt > 30:
                    if pkt_cnt > 150:
                        chk += 4
                    elif pkt_cnt > 110:
                        chk += 2
                    elif pkt_cnt > 90:
                        chk += 1.5
                    elif pkt_cnt > 70:
                        pkt_cnt += 1                        
                    elif pkt_cnt > 40:
                        chk += 0.2
                    else:
                        chk -= 0.2
                else:
                    chk = 0

                if chk >= 4:
                    print("warning: " + str(pkt_cnt))
                    cap = True
                    chk = 0

            pkt_cnt = 0
            pre_time = time

    def cntalert(self): #시야가 오른쪽,왼쪽으로 벗어난 순간 메세지창 띄우기
        global ri_cnt, le_cnt, dw_cnt
        global alert_ri, alert_le, alert_dw
        
        if ri_cnt == 15: # 화면 밖 오른쪽 응시
            #self.save_img() # 이미지 캡쳐
            self.save_mp4(0) # 영상으로 캡처 (로그마다)
            log_msg = "오른쪽을 봤습니다."
            time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            log_list.append([time, log_msg])
            self.alertListWidget.addItem(time + " " + log_msg) # 기록 추가
            self.alertListWidget.scrollToBottom()
            alert_ri += 0.2
            self.alert_show()
            ri_cnt = 0
        elif le_cnt == 15: # 화면 밖 왼쪽 응시
            #self.save_img()
            self.save_mp4(0)
            log_msg = "왼쪽을 봤습니다."
            time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            log_list.append([time, log_msg])
            self.alertListWidget.addItem(time + " " + log_msg)
            self.alertListWidget.scrollToBottom()
            alert_le += 0.2
            self.alert_show()
            le_cnt = 0
        elif dw_cnt == 5: # 아래 응시
            #self.save_img()
            self.save_mp4(0)
            log_msg = "아래를 봤습니다."
            time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            log_list.append([time, log_msg])
            self.alertListWidget.addItem(time + " " + log_msg)
            self.alertListWidget.scrollToBottom()
            alert_dw += 0.2
            self.alert_show()
            dw_cnt = 0

    def alert_show(self): # 경고창 임계값 계산
        global alert_le, alert_ri, alert_dw
        global alert_emp, alert_two
        global alert_int
        global msg
        global yellowcard

        alert_cnt = alert_le + alert_ri + alert_dw + alert_emp + alert_two + alert_int
        print(alert_cnt)
        if alert_cnt >= 1:
            yellowcard += 1
            if yellowcard == 3:
                msg.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
                msg.setText("경고")
                msg.setInformativeText("경고를 3회 무시하여 감독관에게 알림이 갔습니다.")
                msg.exec_()
            else:
                msg.setIconPixmap(QPixmap(settings.img_path + "warning.png").scaled(40, 40))
                msg.setText("경고")
                msg.setInformativeText("의심행위가 반복적으로 탐지됐습니다.\n시험 환경을 점검해주세요.")
                msg.exec_()

            if yellowcard < 3:
                item = QListWidgetItem("⚠ 경고 " + str(yellowcard) + "회 ⚠")
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                item.setFont(font)
                self.alertListWidget.addItem(item)
                self.alertListWidget.scrollToBottom()
            
            alert_le = 0
            alert_ri = 0
            alert_dw = 0
            alert_emp = 0
            alert_two = 0
            alert_int = 0
    
    def save_img(self): # 경고 받으면 캠 캡처 -> 폴더에 날짜와 저장됨
        global frame
        if ret:
            hour = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            filename = "capture/Webcam_{}.png".format(hour)
            cv2.imwrite(filename, frame, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])

    def save_mp4(self, type): # 경고 받으면 영상으로 캡처 -> image폴더에 날짜와 저장됨
        hour = datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")
        filepath = 'capture/Webcam_{}.avi'.format(hour)
        fps = 20.0
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        size = (int(width), int(height))
        out = cv2.VideoWriter(filepath, fourcc, fps, size)
        global frame
        
        save_cnt = 0
        while True:
            ret, frame = webcam.read()
            if ret:
                out.write(frame)
                save_cnt += 1
                if type == 0:
                    if save_cnt == 35:
                        break
                elif type ==1:
                    if save_cnt == 200:
                        break
            else:
                break
        out.release()

    def endWebcam(self):
        self.camLabel.setPixmap(QPixmap(settings.img_path + "cam.png"))
        self.camLabel.setScaledContents(True)
        
        global webcam
        if webcam != None:
            if webcam.isOpened():
                self.stream.close()
                print("stream close")
            webcam.release()
            webcam = None