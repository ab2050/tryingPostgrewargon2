from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("encryptionkey")
fernet = Fernet(key)
#print(Fernet.generate_key().decode())

def encrypt(data):
    if data is None:
        return None
    return fernet.encrypt(data.encode()).decode() #to get a string from the bytes that encode gives

def decrypt(data):
    if data is None:
        return None
    return fernet.decrypt(data.encode()).decode()