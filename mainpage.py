import register
import login
from flask import Flask, render_template, request, redirect, url_for
import adminthings
from passwordAuth import passwordstrength
from entryLogs import successlog,faillog,auditlog
import showgraphs

# username - ad, password - pwd, role - admin
# database= "abcreates",user = "ab",password = "password"

# NEED TO ADD SESSIONS
# user to try redis on - username - user, password - word 
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/existing",methods=["GET","POST"])
def existing():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        result = login.userlogin(name,password)

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
            auditlog.info(f"admin {name} logged in")
            successlog.info(f"Successful login")
            return redirect(url_for("admin"))
        
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

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/users")
def adminusers():
    data = adminthings.showData()
    return render_template("userdata.html",records=data)

@app.route("/admin/logs")
def adminlogs():
    logs = adminthings.showLogs()
    return render_template("logshow.html",records=logs)

@app.route("/admin/analytics")
def adminanalytics():
    graph = showgraphs.analytics()
    return render_template("analytics.html",data=graph)

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