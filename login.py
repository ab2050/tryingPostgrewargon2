from passwordAuth import verify
import dbcreator as dbc
import adminthings as admin
from redisstart import red

#redis running on port 6379
def userlogin(name,password):
    
    conn = dbc.create()
    cursor = conn.cursor()
    
    attemptscount = f"login_attempts-{name}"
    attempts = red.get(attemptscount)

    if attempts is not None and int(attempts)>=3 :
        return "locked_2mins"

    cursor.execute("SELECT password,role FROM storeData WHERE username = %s",(name,)) #issa tuple, idk why
    conn.commit() #might not be necessary

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

            red.delete(attemptscount) #reset the count of failed attempts for every successful login, might need to be tweaked
            return role

        except:
            cursor.execute("INSERT INTO login_logs (username, success) VALUES (%s, %s)",(name, True))
            conn.commit()

            red.incr(attemptscount)
            red.expire(attemptscount,120) 
            #120 seconds = 2 mins, after 2 mins of no login attempts, failed count on redis will get reset, needs to be changed
            return "wrong password"

            #probably should add a name == main