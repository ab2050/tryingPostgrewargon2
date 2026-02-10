from passwordAuth import verify
import dbcreator as dbc
import adminthings as admin

def login():
    name = input("Enter name : ").strip()
    password = input("Enter yer password : ").strip() #need to do the getpass library thing
    role = input("Enter your role : ").strip()
    conn = dbc.create()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM storeData WHERE username = %s",(name,)) #issa tuple, idk why
    conn.commit()

    result = cursor.fetchone() #breaks if i do fetchall :[

    if result is None:
        print("No such user")
        cursor.execute("INSERT INTO login_logs (username, success) VALUES (%s, %s)",(name, False)) #log it
        conn.commit()

    else:
        hash = result[0] #argon2 black magic

        try:
            verify(hash, password) #argon2 returns none if verification is successful, so if conition isn't gonna work
            print("USER AUTHENTICATED")

            cursor.execute("SELECT role FROM storeData WHERE username = %s",(name,))

            a = cursor.fetchone()
            s = a[0] #do this cause a is a TUPLE
            print("USER ROLE IS", s)

            if s.lower()=="admin":
                admin.showrecords()

        except:
            print("Incorrect password")
            cursor.execute("INSERT INTO login_logs (username, success) VALUES (%s, %s)",(name, False))
            conn.commit()

            #probably should add a name == main