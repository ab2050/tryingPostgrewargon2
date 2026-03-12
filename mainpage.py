import register # to allow new users to register, gets register method which hashes password and stores data in postgresql
import login # imports userlogin which verifies password hash, useremail to get user email for MFA
from flask import Flask, render_template, request, redirect, url_for, session #actually stores data
from flask_session import Session #where data is stored, redis or user cookies
import adminthings #admin funcitionalities like show logs, show delete reasons,among others
import passwordAuth #to ensure new users' passwords are strong
from entryLogs import successlog,faillog,auditlog #logs all successes, failures and actions. Audit log is mandated by GDPR
import showgraphs #admin functionality
from sqliteDBforDeleteReason import add_Reason #stores reasons for users leaving
import userActions #currently only allows deleting own data
import os #for dotenv, flask secret key is stored in env for securtiy
from dotenv import load_dotenv #to read .env file
from redisstart import red #gets the connector for redis, session cookies are stored here
from flask_wtf.csrf import CSRFProtect #CSRF protection
import mongoconnect #allows medical staff to store patient health records, and users to add own data
import emails #sends otp via emails
import otp #gets and verifies otp
from datetime import timedelta #for session timeout
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#from mongoconnect import patdata

load_dotenv()
# username - admintrial, password - Word123$%, role - admin || name - usertry/usertry1 ... password - Word123$% role - user
# thedoc, Word123$%, - medical
# database= "abcreates",user = "ab",password = "password"

# NEED TO ADD TALISMAN <- MUST
# ADD A DICTIONARY FOR ALL ERROR CASES AND USER ROLES IN def exisitng()<- MUST
# user to try redis on - username - user, password - word 

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("flaskKey")
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = red #imported from redisstart
app.config["SESSION_USE_SIGNER"] = True #adds an encrypted sign to prevent tampering
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=2)
app.config["SESSION_COOKIE_HTTPONLY"] = True #prevents XSS attacks
app.config["SESSION_COOKIE_SAMESITE"] = "Lax" #prevents BASIC CSRF attacks
app.config["WTF_CSRF_ENABLED"] = True #better CSRF protection, does not rely on browsers

Session(app)
csrf = CSRFProtect(app)

iplimiter = Limiter(get_remote_address, app=app, default_limits=["400 per day"])

@app.before_request
def timeouts():
    if "username" in session or "mfaname" in session:
        session.modified = True
    else:
        if request.endpoint not in ("home","existing","newUser","static","verifyEmail"): #css will break if static not mentioned
            return render_template("Session_Timedout.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/existing",methods=["GET","POST"])
@iplimiter.limit("5 per minute")
def existing():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        result = login.userlogin(name,password)

        # ADD A DICTIONARY FOR ALL ERROR CASES AND USER ROLES <- MUST
        if result == "Invalid username":
            auditlog.info(f"Invalid username attempt from ip : {request.remote_addr}")
            faillog.info(f"Invalid username : {name}")
            return render_template("login.html", error=result)
        
        elif result == "wrong password":
            auditlog.info(f"Invalid password used to access {name} from ip : {request.remote_addr}")
            faillog.info(f"Invalid password used to access {name} from ip : {request.remote_addr}")
            return render_template("login.html", error=result)
        
        elif result == "locked_2mins":
            auditlog.info(f"Account {name} locked, multiple failed attempts")
            faillog.info(f"Multiple failed attempts, lock on user profile {name}")
            return render_template("login.html",error = "Too many failed attempts, retry after 2 mins")
        
        elif result.lower()=="medical":
            session.clear()
            session["username"]=name
            session["role"]="medical"
            auditlog.info(f"Medical staff {name} logged in")
            successlog.info(f"Successful login")
            return redirect(url_for("medic"))
        
        elif result.lower() == "user":
            session.clear()
            session["username"]=name
            session["role"]="user"
            auditlog.info(f"user {name} has logged in")
            successlog.info(f"Successful login")
            return redirect(url_for("users"))
        
        else:
            session.clear() # prevents session fixation attacks,although flask usually does so by itself
            usermail = login.useremail(name)
            code = otp.createOTP(name)
            emails.sendmail(usermail,"Trying out flask logins",f"pyotp generated code is {code}")
            session["mfaname"]=name
            session["mfarole"]=result.lower()
            auditlog.info(f"otp sent to {result.lower()} {name}")
            return redirect(url_for("mfa"))

        '''elif result.lower() == "admin":
            session.clear() #prevents session fixation even though flask generally takes care of it, industry standard practice
            usermail = login.useremail()
            code = otp.createOTP(name)
            emails.sendmail(usermail,"Trying out flask logins",f"pyotp generated code is {code}")
            session["username"]=name
            session["role"]="admin"
            auditlog.info(f"admin {name} logged in")
            successlog.info(f"Successful login")
            return redirect(url_for("admin"))
        
        elif result.lower() == "user":
            session.clear()
            session["username"]=name
            session["role"]="user"
            auditlog.info(f"user {name} has logged in")
            successlog.info(f"Successful login")
            return redirect(url_for("users"))
        
        elif result.lower()=="medical":
            session.clear()
            session["username"]=name
            session["role"]="medical"
            auditlog.info(f"Medical staff {name} logged in")
            successlog.info(f"Successful login")
            return redirect(url_for("medic"))'''
        
    return render_template("login.html")

@app.route("/mfa", methods=["GET","POST"])
@iplimiter.limit("5 per minute")
def mfa():
    if "mfaname" not in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        iotp = request.form["otp"]
        validity = otp.verify(session["mfaname"],iotp)
        name = session["mfaname"]
        role = session["mfarole"]

        if validity=="correct":
            session.pop("mfaname")
            session.pop("mfarole")
            session["username"]=name
            session["role"]=role
            auditlog.info(f"{session["role"]} {session["username"]} verified MFA")

            if role=="admin":     
                successlog.info(f"Successful login")
                return redirect(url_for("admin"))  

            elif role=="user":
                successlog.info(f"Successful login")
                return redirect(url_for("users"))
            
            elif role=="medical":
                successlog.info(f"Successful login")
                return redirect(url_for("medic"))
            
        elif validity=="timedout":
            return render_template("mfa.html",error="Timed out, please re-login")
        elif validity=="wrong":
            return render_template("mfa.html",error= "Wrong otp")
    return render_template("mfa.html")

@app.route("/register", methods = ["GET","POST"])
@iplimiter.limit("5 per minute")
def newUser():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        mail=request.form["email"]

        if not passwordAuth.usernamevalid(name):
            return render_template("register.html",error="Wrong username format")

        if not emails.verifymail(mail):
            return render_template("register.html",error="Wrong email format",name=name)
        
        if passwordAuth.usernameBlacklist(name):
            return render_template("register.html",error="Profanities are not allowed")
        
        if passwordAuth.checkpasswordleaked(password):
            return render_template("register.html",error="Password has already been breached",name=name)
        
        if not passwordAuth.passwordstrength(password):
            return render_template("register.html",error="Password not strong",name=name)
        
        token = emails.createToken(name,password,mail)
        link = url_for("verifyEmail",token=token,_external=True)
        emails.sendmail(mail,"Gotta verify",f"My own university trial so click on {link}")
        auditlog.info(f"Verification email sent to {name}")
        return render_template("register.html",message="check email, click link",name=name)

        '''adduser = register.register(name,password,mail)

        if adduser:
            auditlog.info(f"New user {name} added")
            return render_template("added.html")

        else:
            return render_template("register.html", error="Username already taken")'''
        
    return render_template("register.html")

@app.route("/verify/<token>")
def verifyEmail(token):
    data = emails.verifyToken(token)
    if data:
        register.register(data["username"],data["password"],data["email"])
        auditlog.info(f"{data["username"]} account created")
        return render_template("verified.html",message="Your email has been verified, welcome aboard !")
    return render_template("verified.html",error="Invalid link")

@app.route("/user")
def users():
    if "username" not in session: # session is kinda like a dictionary, checks if the session has a username to avoid 
        #someone just pasting in the link
        return redirect(url_for("home"))
    return render_template("users.html")

@app.route("/user/upload", methods=["GET","POST"])
def userAddsData():
    if "username" not in session or session.get("role") !="user": #show flash message
        return redirect(url_for("home")),403
    
    if request.method== "POST":
        mongoconnect.patientAddsData(session["username"],request.form["name"],request.form["age"])

        return redirect(url_for("users"))
    return render_template("patient_upload.html")

@app.route("/user/view")
def userViewsData():
    if "username" not in session or session.get("role")!="user":
        return redirect(url_for("home"))
    
    return render_template("User_View_Records.html",record=mongoconnect.individual(session["username"]))

@app.route("/admin")
def admin():
    if "username" not in session:
        return redirect(url_for("home"))
    
    if session.get("role")!="admin":
        return render_template("Error403.html"),403 #industry standard i guess
    return render_template("admin.html")

@app.route("/admin/userDeleted")
def adminUserExitReason():
    if "username" not in session:
        return redirect(url_for("home"))
    
    if session.get("role")!="admin":
        return render_template("Error403.html"),403
    reason = adminthings.showDeleteReasons()
    auditlog.info(f"Admin viewed deletion reasons from ip {request.remote_addr}")
    return render_template("delete_reasons.html", reasons=reason)

@app.route("/admin/users")
def adminusers():
    if "username" not in session:
        return redirect(url_for("home"))
    
    if session.get("role")!="admin":
        return render_template("Error403.html"),403
    data = adminthings.showData()
    return render_template("userdata.html",records=data)

@app.route("/admin/logs")
def adminlogs():
    if "username" not in session:
        return redirect(url_for("home"))
    
    if session.get("role")!="admin":
        return render_template("Error403.html"),403
    logs = adminthings.showLogs()
    return render_template("logshow.html",records=logs)

@app.route("/admin/analytics")
def adminanalytics():
    if "username" not in session:
        return redirect(url_for("home"))
    
    if session.get("role")!="admin":
        return render_template("Error403.html"),403
    graph = showgraphs.analytics()
    return render_template("analytics.html",data=graph)

@app.route("/medic")
def medic():
    if "username" not in session:
        return redirect(url_for("home"))
    return render_template("medic.html")

@app.route("/medic/edit", methods=["GET","POST"])
def medEditsData():
    if "username" not in session or session.get("role")!="medical":
        return redirect(url_for("home"))
    if request.method=="POST":
        data ={
            "username":request.form["username"],
            "disease":request.form["disease"],
            "medicines":request.form["medicines"],
            "notes":request.form["notes"]
        }
        mongoconnect.medAddsData(data)
        return redirect(url_for("medic"))
    return render_template("medic_upload.html")

@app.route("/medic/view")
def medViewsData():
    if "username" not in session or session.get("role") != "medical":
        return redirect(url_for("home"))
    
    records = mongoconnect.showpatients()
    return render_template("Med_Views_data.html",record=records)

@app.route("/medic/testview")
def medtest():
    if "username" not in session or session.get("role") != "medical":
        return redirect(url_for("home"))
    
    records = mongoconnect.checkencryption()
    return render_template("Med_Views_data.html",record=records)

@app.route("/delete",methods=["GET","POST"])
def userDelete():
    if "username" not in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        name = session["username"]
        reason = request.form.get("reason", "") # in case user does not give a reason

        auditlog.info(f"User {name} deleted their account")
        add_Reason(reason)
        userActions.deleteData(name)

        return render_template("deleted.html")
    return render_template("delete_account.html")

@app.route("/logout")
def logout():
    name = session.get("username")
    session.clear()
    auditlog.info(f"{name} logged out")
    return redirect(url_for("home"))

if __name__ == "__main__": #otherwise tests will freeze
    app.run(debug=True)
'''n = input("HI, EXISTING USER (1) OR WANNA CREATE A NEW ONE (2) ? (1/2)")

if not n.isdigit():
    print("NAH MAN GOTTA GIVE 1/2")
    exit()

elif int(n) == 2:
    register.register()

elif int(n)==1:
    login.login()

else:
    print("1 OR 2 MAN")'''