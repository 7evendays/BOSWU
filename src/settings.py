import pyrebase
import json
from requests import get

with open("firebase/auth.json") as f:
            config = json.load(f)
firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
# Get a reference to the database service
db = firebase.database()
host_ip = get("https://api.ipify.org").text.split(".")
del(host_ip[3])
host_ip = ".".join(host_ip)

class settings():
    global login
    global uid
    global email
    global uname
    global sid
    global major
    global verified

    def initialInfo():
        settings.login = False
        settings.uid = None
        settings.email = None
        settings.uname = None
        settings.sid = None
        settings.major = None
        settings.ip = None

    def setInfo():
        settings.uid = settings.login["localId"]
        db.child("users").child(settings.uid).update({
            "login": True,
            "ip": host_ip
        })
        settings.email = db.child("users").child(settings.uid).child("email").get().val()
        settings.uname = db.child("users").child(settings.uid).child("name").get().val()
        settings.sid = db.child("users").child(settings.uid).child("sid").get().val()
        settings.major = db.child("users").child(settings.uid).child("major").get().val()
        settings.ip = db.child("users").child(settings.uid).child("ip").get().val()

    def expireInfo():
        if settings.login != False:
            db.child("users").child(settings.uid).update({
                "login": False,
                "ip": None
            })
            settings.initialInfo()