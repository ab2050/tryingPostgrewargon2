#create the 2 tables
import psycopg2

def create():
    conn = psycopg2.connect(database= "abcreates",user = "ab",password = "password",host = "localhost",port = "5432")
    return conn #easier to just return it 

def makeTables():
    conn = create()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE if not exists storeData (user_id SERIAL PRIMARY KEY,username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,role TEXT NOT NULL,failed_attempts INT DEFAULT 0,locked BOOLEAN DEFAULT FALSE )""")

    cursor.execute("""CREATE TABLE if not exists login_logs (
    log_id SERIAL PRIMARY KEY,username TEXT,success BOOLEAN,timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP) """)

    conn.commit()#won't get stored in db otherwise :(

    cursor.close() #must in this very order, closing conn should automatically close cursor, but gotta be professional
    conn.close()

def make(name,password,role): #gotta remove the role
    conn = create()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM storeData where username = %s",(name,))
    if cursor.fetchone():
        return False

    cursor.execute("INSERT INTO storeData (username, password, role) VALUES (%s, %s, %s)",(name, password, role))
    conn.commit() #use try catch in case same name comes in (will change primary key later if the weather is nice)
    print("User has been added")

    cursor.close()
    conn.close()

def show():
    conn = create()
    cursor = conn.cursor()

    cursor.execute("select * from storeData")
    conn.commit()
    data = cursor.fetchall() #only cursor.fetchall won't do shit, ask me how i know
    for data in data: #python has no issue with this apparently
        print(data)

    cursor.close()
    conn.close()

def show_logs():
    conn = create()
    cursor = conn.cursor()

    cursor.execute("select * from login_logs")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    #create()
    makeTables() #get a better way to create the tables
    print("Tables have been created")