import pyrebase
import json
import socket
from requests import get


class settings():
    global login
    global uid
    global email
    global uname
    global sid
    global major
    global verified
    global ref
    global r_std
    global l_std
    global d_std

    img_path = "src/imgsource/"

    with open("firebase/auth.json") as f:
            config = json.load(f)
    firebase = pyrebase.initialize_app(config)
    # Get a reference to the auth service
    auth = firebase.auth()
    # Get a reference to the database service
    db = firebase.database()
    
    #host_ip = get("https://api.ipify.org").text.split(".")
    #del(host_ip[3])
    #host_ip = ".".join(host_ip)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    HOST = sock.getsockname()[0].split(".")
    sock.close()

    del(HOST[3])
    HOST = ".".join(HOST)

        
    def initialInfo():
        settings.login = False
        settings.uid = None
        settings.admin = False
        settings.email = None
        settings.uname = None
        settings.sid = None
        settings.major = None
        settings.ip = None
        settings.r_std = 0.42
        settings.l_std = 0.66
        settings.d_std = 0.64
        
    def setInfo():
        settings.uid = settings.login["localId"]
        settings.db.child("users").child(settings.uid).update({
            "login": True,
            "ip": settings.HOST
        })
        settings.admin = settings.db.child("users").child(settings.uid).child("admin").get().val()
        settings.sid = settings.db.child("users").child(settings.uid).child("sid").get().val()
        settings.r_std = settings.db.child("users").child(settings.uid).child("eye").child("r_std").get().val()
        settings.l_std = settings.db.child("users").child(settings.uid).child("eye").child("l_std").get().val()
        settings.d_std = settings.db.child("users").child(settings.uid).child("eye").child("d_std").get().val()

        settings.email = settings.db.child("users").child(settings.uid).child("email").get().val()
        settings.uname = settings.db.child("users").child(settings.uid).child("name").get().val()
        settings.major = settings.db.child("users").child(settings.uid).child("major").get().val()
        settings.ip = settings.db.child("users").child(settings.uid).child("ip").get().val()
        
        
    def updatecali(r_std, l_std, d_std):
        settings.uid = settings.login["localId"]
        
        settings.db.child("users").child(settings.uid).child("eye").update({
            "r_std": round(r_std, 2),
            "l_std": round(l_std, 2),
            "d_std": round(d_std, 2)
        })
        settings.r_std = r_std
        settings.l_std = l_std
        settings.d_std = d_std

    def expireInfo():
        if settings.login != False:
            settings.db.child("users").child(settings.uid).update({
                "login": False,
                "ip": None
            })
            settings.initialInfo()