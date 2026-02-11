import register
import login
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/existing")
def existing():
    login.login()

@app.route("/register", methods = ["GET","POST"])
def newUser():

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        adduser = register.register(name,password)

        if adduser:
            return render_template("added.html")
        
        if not adduser:
            return render_template("register.html",error="Username already taken")

        return redirect({url_for("home")})
    return render_template("register.html")

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