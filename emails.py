import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import re
import secrets
import json
from redisstart import red

load_dotenv()
pwd = os.getenv("appPassword")
emailid = os.getenv("emailid")

def createToken(name,pwd,email):
    token = secrets.token_urlsafe(32)
    data = json.dumps({"username":name,"password":pwd,"email":email})
    red.setex(f"verify:{token}",180,data)
    return token

def verifyToken(token):
    data = red.get(f"verify:{token}")
    if data:
        red.delete(f"verify:{token}")
        return json.loads(data.decode())
    return None

def sendmail(to,subject,body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = emailid
    msg["To"] = to

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(emailid, pwd)
        server.send_message(msg)

#rec = os.getenv("receivermail")
#print(rec)
#sendmail(rec,"Checking flask again","Sending myself this email")

def verifymail(usermail):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern,usermail) is not None