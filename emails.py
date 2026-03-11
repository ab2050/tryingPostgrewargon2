import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import re
load_dotenv()
pwd = os.getenv("appPassword")
emailid = os.getenv("emailid")

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