from passwordAuth import verify
import dbcreator as dbc
import adminthings as admin

def userlogin(name,password):
    
    conn = dbc.create()
    cursor = conn.cursor()

    cursor.execute("SELECT password,role FROM storeData WHERE username = %s",(name,)) #issa tuple, idk why
    conn.commit()

    result = cursor.fetchone() #breaks if i do fetchall :[

    if result is None:
        cursor.execute("INSERT INTO login_logs (username, success) VALUES (%s, %s)",(name, False)) #log it
        conn.commit()
        return "Invalid username"

    else: #consider removing the else later
        hash = result[0]
        role = result[1]

        try:
            verify(hash, password) #argon2 returns none if verification is successful, so if conition isn't gonna work
            cursor.execute("INSERT INTO login_logs (username, success) VALUES (%s, %s)",(name, True))
            conn.commit()

            return role

        except:
            cursor.execute("INSERT INTO login_logs (username, success) VALUES (%s, %s)",(name, True))
            conn.commit()

            return "wrong password"

            #probably should add a name == main