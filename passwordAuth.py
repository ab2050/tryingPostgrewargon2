import argon2
from argon2 import PasswordHasher

ph = PasswordHasher() #can edit salt length and all, but don't think its necessary

def store(password):
    return ph.hash(password)

def verify(hash,password):
    ph.verify(hash,password)