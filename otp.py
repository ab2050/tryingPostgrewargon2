import pyotp
from redisstart import red

def createOTP(username):
    otp = pyotp.TOTP(pyotp.random_base32(),interval=180) #otp lasts for 3 mins
    otp = otp.now()
    red.setex(f"otp:{username}",180,otp)
    return otp

def verify(username, rotp):
    otp = red.get(f"otp:{username}")
    if otp is None:
        return "timedout"
    if otp.decode() == rotp:
        red.delete(f"otp:{username}")
        return "correct"
    return "wrong"