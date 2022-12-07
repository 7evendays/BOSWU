import cv2, qimage2ndarray
import mediapipe as mp
from requests import get
from scapy.all import *
from PIL import ImageGrab
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyrebase
import json
from src.settings import *
from eyetracking.gaze_tracking import GazeTracking
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
img_path = "src/imgsource/"
webcam = None
global log_list
log_list = []
ri_cnt = 0
le_cnt = 0
alert_cnt = 0
alert_le = 0
alert_ri = 0
alert_emp = 0
alert_two = 0
alert_int = 0
yellowcard = 0
protocols = {1: 'ICMP', 6: 'TCP', 17:'UDP'}
global pre_time, pkt_cnt, pre_cnt, cap, approv, chk, start_time
pre_time = datetime.now()
pkt_cnt = 0
pre_cnt = 0
lock = threading.Lock()
approv = False
cap = False
chk = 0
HOST = socket.gethostbyname(socket.gethostname())
with open("firebase/auth.json") as f:
            config = json.load(f)
firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
# Get a reference to the database service
db = firebase.database()
global group
group = False

class ExamDialog(QDialog):
    def __init__(self):
        super(ExamDialog, self).__init__()
        self.setupUI()
        
    def closeEvent(self, event):
        self.endWebcam()

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(ExamDialog, self).keyPressEvent(event)
        
    def setupUI(self):
        self.resize(720, 480)
        self.setWindowTitle("ChasEye 체이스아이 :: 시험")
        self.setWindowIcon(QIcon(img_path + "icon.png"))
        
        # basic font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")

        # label for header
        self.headerLabel = QLabel("방ID - 과목명")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.headerLabel.setFixedHeight(40) # 높이 고정
        self.headerLabel.setSizePolicy(sizePolicy) # 너비 확장 높이 고정
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.headerLabel.setFont(font)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter) # 가운데 정렬
        self.headerLabel.setStyleSheet("background-color: #07A3B7;\n"
                                       "color: #FFF;\n"
                                       "border-radius: 10px;\n")
        
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.camLabel.setMinimumSize(QtCore.QSize(640, 480)) # 최소 사이즈(너비, 높이)
        self.camLabel.setSizePolicy(sizePolicy)
        self.camLabel.setPixmap(QtGui.QPixmap(img_path + "cam.png"))
        self.camLabel.setScaledContents(True) # 이미지 크기 조정

        # button size policy
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed) # 너비 확장 높이 고정
        
        # button font policy
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        
        # button for turn on camera
        self.camonBtn = QPushButton("카메라 켜기")
        self.camonBtn.setMaximumWidth(480) # 최대 너비
        self.camonBtn.setFixedHeight(30) # 높이 고정
        self.camonBtn.setSizePolicy(sizePolicy)
        self.camonBtn.setFont(font)
        self.camonBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.camonBtn.setStyleSheet("background-color : #07A3B7;\n"
                                    "color : #FFF;\n"
                                    "border-radius : 10px;\n"
                                    "padding: 4px;\n")
        self.camonBtn.clicked.connect(self.camonBtnClicked)
        
        # button for turn off camera
        self.camoffBtn = QPushButton("카메라 끄기")
        self.camoffBtn.setMaximumWidth(480) # 최대 너비
        self.camoffBtn.setFixedHeight(30) # 높이 고정
        self.camoffBtn.setSizePolicy(sizePolicy)
        self.camoffBtn.setFont(font)
        self.camoffBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.camoffBtn.setStyleSheet("background-color : #07A3B7;\n"
                                     "color : #FFF;\n"
                                     "border-radius : 10px;\n")
        self.camoffBtn.clicked.connect(self.camoffBtnClicked)

        # button for go back
        self.gobackBtn = QPushButton("뒤로 가기")
        self.gobackBtn.setMaximumWidth(480) # 최대 너비
        self.gobackBtn.setFixedHeight(30) # 높이 고정
        self.gobackBtn.setSizePolicy(sizePolicy)
        self.gobackBtn.setFont(font)
        self.gobackBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # 커서
        self.gobackBtn.setStyleSheet(#"background-color : #DAEBC7;\n"
                                     "color : #07A3B7;\n"
                                     "border : 2px solid #07A3B7;\n"
                                     "border-radius : 10px;\n"
                                     "padding: 4px;\n")
        self.gobackBtn.clicked.connect(self.gobackBtnClicked)

        # set layout
        # outerLayout: QVBox
        # ㄴ hearderLabel
        # ㄴ innerLayout: QHBox
        #    ㄴ camlabel
        #    ㄴ innerRightLayout: QVBox
        #       ㄴ alertLayout: QVBox
        #          ㄴ alertTitleLabel
        #          ㄴ aletListWidget
        #       ㄴ buttonLayout: QVBox
        outerLayout = QVBoxLayout(self)
        outerLayout.setContentsMargins(8, 8, 8, 8)
        outerLayout.setSpacing(8)
        innerLayout = QHBoxLayout()
        innerLayout.setSpacing(4)
        innerRightLayout = QVBoxLayout()
        alertLayout = QVBoxLayout()
        alertLayout.setContentsMargins(0, 0, 0, 8)
        alertLayout.setSpacing(4)
        buttonLayout = QVBoxLayout()
        
        outerLayout.addWidget(self.headerLabel)
        outerLayout.addLayout(innerLayout)
        innerLayout.addWidget(self.camLabel)
        innerLayout.addLayout(innerRightLayout)
        innerRightLayout.addLayout(alertLayout)
        innerRightLayout.addLayout(buttonLayout)
        alertLayout.addWidget(self.alertTitleLabel)
        alertLayout.addWidget(self.alertListWidget)
        buttonLayout.addWidget(self.camonBtn)
        buttonLayout.addWidget(self.camoffBtn)
        buttonLayout.addWidget(self.gobackBtn)

    def gobackBtnClicked(self):
        if not (webcam == None):
            webcam.release()
        self.alertListWidget.clear()
        self.close()

    def camonBtnClicked(self):
        self.startWebcam()

    def camoffBtnClicked(self):
        self.endWebcam()

    def startWebcam(self):
        global start_time
        start_time = datetime.now()

        global webcam
        webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 0번 카메라 장치 연결
        #webcam.set(cv2.CAP_PROP_FPS, 10) # 프레임 수를 낮추고 싶으면 주석 해제
        
        global gaze
        gaze = GazeTracking()
        e_alert_time = datetime.now()
        t_alert_time = datetime.now()
        
        global msg
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(img_path + "alert.png"))
        msg.setWindowTitle("알림")
        
        """
        # Left eye indices list
        LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
        # Right eye indices list
        RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]
        LEFT_IRIS = [474,475, 476, 477]
        RIGHT_IRIS = [469, 470, 471, 472]
        """
        self.stream = db.child("users").stream(self.stream_handler)
        
        try:
            while webcam.isOpened():
                # We get a new frame from the webcam
                global ret, frame
                global alert_le, alert_ri, alert_emp, alert_two
                ret, frame = webcam.read()

                # 만약 카메라가 연결되어 있지 않으면 while 반복문 종료
                if not ret:
                    msg.setIconPixmap(QPixmap(img_path + "info.png").scaled(40, 40))
                    msg.setText("오류")
                    msg.setInformativeText("웹캠을 찾을 수 없습니다.")
                    msg.exec_()
                    self.endWebcam()
                    break

                # 보기 편하기 위해 이미지를 좌우를 반전하고, BGR 이미지를 RGB로 변환
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 성능을 향상시키려면 이미지를 작성 여부를 False으로 설정
                # 영상에 얼굴 감지 주석 그리기 기본값 : True
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                #getting width and height or frame
                #img_h, img_w = frame.shape[:2]
                
                with mp_face_detection.FaceDetection( #얼굴인식
                    model_selection = 0,
                    min_detection_confidence = 0.5
                    ) as face_detection:
                        d_results = face_detection.process(frame)

                        # 자리 비움 감지
                        if d_results.detections: # 사람 있음
                            #for detection in d_results.detections: # 주석 그리기
                                #mp_drawing.draw_detection(frame, detection)
                            if len(d_results.detections) >= 2: # 사람 2명 이상
                                if ((datetime.now() - t_alert_time).seconds) > 10:                                #self.save_img() # 이미지 저장을 원하면 주석 해제
                                    self.save_mp4() # 동영상 저장을 원하면 주석 해제
                                    alert_two += 0.4
                                    log_msg = "외부인이 감지됐습니다."
                                    time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
                                    log_list.append(time + " " +log_msg)
                                    self.alertListWidget.addItem(time + " " + log_msg)
                                    self.alertListWidget.scrollToBottom()
                                    self.alert_show()
                                t_alert_time = datetime.now()
                        else: # 사람 없음
                            if ((datetime.now() - e_alert_time).seconds) > 10:
                                #self.save_img() # 이미지 저장을 원하면 주석 해제
                                self.save_mp4() # 동영상 저장을 원하면 주석 해제
                                alert_emp += 0.4
                                log_msg = "자리를 비우지 마세요."
                                time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
                                log_list.append(time + " " +log_msg)
                                self.alertListWidget.addItem(time + " " +log_msg)
                                self.alertListWidget.scrollToBottom()
                                self.alert_show()
                            e_alert_time = datetime.now()

                # GazeTracking
                # We send this frame to GazeTracking to analyze it
                gaze.refresh(frame)
                frame = gaze.annotated_frame()

                Hdir = "horizontal direction"
                Vdir = "vertical direction"
                if gaze.is_right():
                    Hdir = "Looking right"
                    global ri_cnt
                    ri_temp = ri_cnt
                    ri_temp += 1
                    ri_cnt = ri_temp
                    self.vision_track()
                elif gaze.is_left():
                    Hdir = "Looking left"
                    global le_cnt
                    le_temp = le_cnt
                    le_temp += 1
                    le_cnt = le_temp
                    self.vision_track()
                elif gaze.is_center():
                    Hdir = "Looking center"
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                """
                cv2.putText(frame, Hdir, (90, 400), cv2.FONT_HERSHEY_DUPLEX, 1.2, (7, 163, 183), 2)
                cv2.putText(frame, Vdir, (90, 450), cv2.FONT_HERSHEY_DUPLEX, 1.2, (7, 163, 183), 2)
                left_pupil = gaze.pupil_left_coords()
                right_pupil = gaze.pupil_right_coords()
                down_pupil = gaze.pupil_down_coords()
                cv2.putText(frame, "left pupil:  " + str(left_pupil), (340, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (7, 163, 183), 1)
                cv2.putText(frame, "right pupil: " + str(right_pupil), (340, 85), cv2.FONT_HERSHEY_DUPLEX, 0.8, (7, 163, 183), 1)
                cv2.putText(frame, "is down: " + str(down_pupil), (340, 120), cv2.FONT_HERSHEY_DUPLEX, 0.8, (7, 163, 183), 1)
                """

                """
                # mediapipe iris
                with mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.6,
                    min_tracking_confidence=0.6
                ) as face_mesh:
                    m_results = face_mesh.process(frame)
                    if m_results.multi_face_landmarks:
                        mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                        for p in m_results.multi_face_landmarks[0].landmark])
                    
                        (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                        # turn center points into np array 
                        center_left = np.array([l_cx, l_cy], dtype=np.int32)
                        center_right = np.array([r_cx, r_cy], dtype=np.int32)
                        
                        # iris
                        cv2.circle(frame, center_left, int(l_radius), (255,0,255), 2, cv2.LINE_AA)
                        cv2.circle(frame, center_right, int(r_radius), (255,0,255), 2, cv2.LINE_AA)
                """

                #image = qimage2ndarray.array2qimage(cv2.flip(frame, 1)) # 이미지 반전을 원하면 주석을 해제
                image = qimage2ndarray.array2qimage(frame)
                self.camLabel.setPixmap(QPixmap(image))
                self.camLabel.setScaledContents(True) # 레이블이 사용 가능한 모든 공간을 채우기 위해 내용의 크기를 조정할지를 설정
                
                global cap, alert_int

                #lock.acquire()
                #threading.Thread(target = self.pktcap).start()
                #lock.release()
                #threading.Thread(target = self.printcnt).start()

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

                global group
                if group == True:
                    self.save_mp4()
                    group = False

                if cv2.waitKey(10) == ord('q'):
                    self.endWebcam()
                    break
        except:
            settings.expireInfo()
            print("Exiting")

    def stream_handler(self, message):
        # We only care if something changed
        if message["event"] in ("put", "patch"):
            print("Something changed")
            self.chkgrouptest()

    def chkgrouptest(self):
        host_ip = settings.ip
        ip_list = []
        
        all_users = db.child("users").get()
        for user in all_users.each():
            uid = user.key()
            if uid != settings.uid:
                login = db.child("users").child(uid).child("login").get().val()
                if login == True:
                    ip_list.append(db.child("users").child(uid).child("ip").get().val())
        print(ip_list)
        
        cnt_ip = ip_list.count(host_ip)
        if cnt_ip > 0:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(img_path + "alert.png"))
            msg.setWindowTitle("알림")
            msg.setIconPixmap(QPixmap(img_path + "warning.png").scaled(40, 40))
            msg.setText("경고")
            msg.setInformativeText("같은 장소에 타응시생이 있음이 감지되어 감독관에게 알림이 갔습니다.\n"
                                   "지금부터 카메라를 이용하여 주변을 360도 각도로 촬영하여 사람이 없음을 녹화해주세요."
                                   "OK 버튼을 누르면 자동으로 10초간 녹화가 진행됩니다.\n"
                                   "※ 녹화를 하지 않을 시 추후에 불이익이 발생할 수 있습니다.")
            msg.exec_()
            global group
            group = True

    def pktcap(self):
        sniff(filter = "ip", prn = self.cntpacket, count = 5)

    def cntpacket(self, packet):
        global pkt_cnt, pre_time, approv, HOST, start_time
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
                        approv = False

    def printcnt(self):
        global pkt_cnt, pre_cnt, pre_time, cap, approv, chk
        time = datetime.now()

        if (time - pre_time).seconds > 1:
            print(pkt_cnt)
            
            if approv == True:
                approv = False
            else:
                if pkt_cnt > 140:
                    chk += 4
                elif pkt_cnt > 110:
                    chk += 3
                elif pkt_cnt > 80:
                    chk += 2
                elif pkt_cnt > 60:
                    chk += 1.5
                elif pkt_cnt > 30:
                    chk += 1
                else:
                    chk = 0

                if chk >= 1000:
                    print("warning: " + str(pkt_cnt))
                    cap = True
                    chk = 0

            pkt_cnt = 0
            pre_time = time

    def vision_track(self): #시야가 오른쪽,왼쪽으로 벗어난 순간 메세지창 띄우기
        global ri_cnt, le_cnt
        global alert_ri, alert_le
        
        if ri_cnt == 10: #오른쪽으로 벗어난 경우 
            #self.save_img() # 이미지 캡쳐
            self.save_mp4() # 영상으로 캡처 (로그마다)
            log_msg = "오른쪽을 봤습니다."
            time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            log_list.append([time, log_msg])
            self.alertListWidget.addItem(time + " " + log_msg) # 기록 추가
            self.alertListWidget.scrollToBottom()
            alert_ri += 0.3
            self.alert_show()
            ri_cnt = 0
        elif le_cnt == 10: #왼쪽으로 벗어난 경우
            #self.save_img()
            self.save_mp4()
            log_msg = "왼쪽을 봤습니다."
            time = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            log_list.append([time, log_msg])
            self.alertListWidget.addItem(time + " " + log_msg)
            self.alertListWidget.scrollToBottom()
            alert_le += 0.2
            self.alert_show()
            le_cnt = 0

    def alert_show(self): # 경고창 임계값 계산
        global alert_le, alert_ri
        global alert_emp, alert_two
        global alert_int
        global msg
        global yellowcard

        alert_cnt = alert_le + alert_ri + alert_emp + alert_two + alert_int
        print(alert_cnt)
        if alert_cnt >= 1:
            yellowcard += 1
            if yellowcard == 3:
                msg.setIconPixmap(QPixmap(img_path + "warning.png").scaled(40, 40))
                msg.setText("경고")
                msg.setInformativeText("경고를 3회 이상 무시하여 감독관에게 알림이 갔습니다.")
                msg.exec_()
            else:
                msg.setIconPixmap(QPixmap(img_path + "warning.png").scaled(40, 40))
                msg.setText("경고")
                msg.setInformativeText("의심행위가 반복적으로 탐지됐습니다.\n시험 환경을 점검해주세요.")
                msg.exec_()

            item = QListWidgetItem("⚠ 경고 " + str(yellowcard) + "회 ⚠")
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setBold(True)
            item.setFont(font)
            self.alertListWidget.addItem(item)
            self.alertListWidget.scrollToBottom()
            
            alert_le = 0
            alert_ri = 0
            alert_emp = 0
            alert_two = 0
            alert_int = 0
    
    def save_img(self): # 경고 받으면 캠 캡처 -> 폴더에 날짜와 저장됨
        global frame
        if ret:
            hour = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
            filename = "capture/Webcam_{}.png".format(hour)
            cv2.imwrite(filename, frame, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])

    def save_mp4(self): # 경고 받으면 영상으로 캡처 -> image폴더에 날짜와 저장됨
        hour = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
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
                if save_cnt == 35:
                    break
            else:
                break
        out.release()

    def save_mp4_long(self): # 경고 받으면 영상으로 캡처 -> image폴더에 날짜와 저장됨
        hour = datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
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
                if save_cnt == 50:
                    msg = QMessageBox()
                    msg.setWindowIcon(QIcon(img_path + "alert.png"))
                    msg.setWindowTitle("알림")
                    msg.setIconPixmap(QPixmap(img_path + "warning.png").scaled(40, 40))
                    msg.setText("경고")
                    msg.setInformativeText("녹화가 완료되었습니다.")
                    break
            else:
                break
        out.release()

    def endWebcam(self):
        self.camLabel.setPixmap(QPixmap(img_path + "cam.png"))
        self.camLabel.setScaledContents(True)
        
        if webcam != None:
            webcam.release()