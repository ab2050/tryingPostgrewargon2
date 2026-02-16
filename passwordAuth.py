import argon2
from argon2 import PasswordHasher


ph = PasswordHasher() #can edit salt length and all, but I don't think its necessary

def store(password):
    return ph.hash(password)

def verify(hash,password):
    ph.verify(hash,password)

def passwordstrength(pwd):
    import re

    passwordpattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$" 
    #\W_ allows all special characters, ? = is lookup to ensure that all these are present
    #p = r"^(?=.*[a-zA-Z\d]).{8,}$" does not work, it just checks if its 8 chars long and has any one of the 3,
    #that is lowercase uppercase or digit, if you put 1234567890 it will take it
    return re.match(passwordpattern,pwd)