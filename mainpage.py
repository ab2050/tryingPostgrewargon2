import register
import login
from flask import Flask, render_template, request, redirect, url_for
import adminthings

# username - adm, password - pwd, role - admin
# database= "abcreates",user = "ab",password = "password"
 
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
            return render_template("login.html", error=result)
        
        elif result == "wrong password":
            return render_template("login.html", error=result)

        elif result.lower() == "admin":
            return redirect(url_for("admin"))
    return render_template("login.html")

@app.route("/register", methods = ["GET","POST"])
def newUser():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        adduser = register.register(name,password)

        if adduser:
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