import register
import login
from flask import Flask, render_template, request, redirect, url_for, session #actually stores data
from flask_session import Session #where data is stored, redis or user cookies
import adminthings
from passwordAuth import passwordstrength
from entryLogs import successlog,faillog,auditlog
import showgraphs
from sqliteDBforDeleteReason import add_Reason
import userActions
import os
from dotenv import load_dotenv
from redisstart import red
from flask_wtf.csrf import CSRFProtect

load_dotenv()
# username - admintrial, password - Word123$%, role - admin || name - gen password - Word123$% role - user
# database= "abcreates",user = "ab",password = "password"

# NEED TO ADD TALISMAN <- MUST
# ADD A DICTIONARY FOR ALL ERROR CASES AND USER ROLES IN def exisitng()<- MUST
# user to try redis on - username - user, password - word 

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("flaskKey")
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = red #imported from redisstart
app.config["SESSION_USE_SIGNER"] = True #adds an encrypted sign to prevent tampering
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True #prevents XSS attacks
app.config["SESSION_COOKIE_SAMESITE"] = "Lax" #prevents BASIC CSRF attacks
app.config["WTF_CSRF_ENABLED"] = True #better CSRF protection, does not rely on browsers

Session(app)
csrf = CSRFProtect(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/existing",methods=["GET","POST"])
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

        elif result.lower() == "admin":
            session.clear() #prevents session fixation even though flask generally takes care of it, industry standard practice
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
        
    return render_template("login.html")

@app.route("/register", methods = ["GET","POST"])
def newUser():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        if not passwordstrength(password):
            return render_template("register.html",error="Password not strong",name=name)

        adduser = register.register(name,password)

        if adduser:
            auditlog.info(f"New user {name} added")
            return render_template("added.html")

        else:
            return render_template("register.html", error="Username already taken")
        
    return render_template("register.html")

@app.route("/user")
def users():
    if "username" not in session: # session is kinda like a dictionary, checks if the session has a username to avoid 
        #someone just pasting in the link
        return redirect(url_for("home"))
    return render_template("users.html")

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