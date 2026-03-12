import argon2
from argon2 import PasswordHasher
import re
import httpx
import hashlib
from better_profanity import profanity

ph = PasswordHasher() #can edit salt length and all, but I don't think its necessary

def store(password):
    return ph.hash(password)

def verify(hash,password):
    ph.verify(hash,password)

def passwordstrength(pwd):
    
    passwordpattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$" 
    #\W_ allows all special characters, ? = is lookup to ensure that all these are present
    #p = r"^(?=.*[a-zA-Z\d]).{8,}$" does not work, it just checks ts 8 chars long and has any one of the 3,
    #that is lowercase uppercase or digit, if you put 1234567890 it will if take it
    return re.match(passwordpattern,pwd)

def checkpasswordleaked(password):
    sha = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha[:5]
    suffix = sha[5:]
    check = httpx.get(f"https://api.pwnedpasswords.com/range/{prefix}") #k-anonymity concept, only sending the first 5 letters
    hashes = (line.split(":") for line in check.text.splitlines())
    for hash,count in hashes:
        if hash == suffix: #api will only return hashes that have the same first 5 that we sent
            return True
    return False        

def usernamevalid(username):
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    return re.match(pattern,username) is not None

def usernameBlacklist(username):
    return profanity.contains_profanity(username)