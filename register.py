import dbcreator as dbc
from passwordAuth import store
import getpass #hides password when typing in, need to implement in login.py

def register():
    name = input("Enter name : ").strip() #name is currently primary key, gotta change that
    password = getpass.getpass("Enter yer password : ").strip()
    role = "Admin" #Just to test adminthings.py

    password = store(password)
    dbc.make(name,password,role)