import pyrebase
import json

with open("firebase/auth.json") as f:
            config = json.load(f)
firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
# Get a reference to the database service
db = firebase.database()

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

    def setInfo():
        settings.uid = settings.login["localId"]
        db.child("users").child(settings.uid).update({
            "login": True
        })
        settings.email = db.child("users").child(settings.uid).child("email").get().val()
        settings.uname = db.child("users").child(settings.uid).child("name").get().val()
        settings.sid = db.child("users").child(settings.uid).child("sid").get().val()
        settings.major = db.child("users").child(settings.uid).child("major").get().val()
    
    def expireInfo():
        if settings.login != False:
            db.child("users").child(settings.uid).update({
                "login": False
            })
            settings.initialInfo()