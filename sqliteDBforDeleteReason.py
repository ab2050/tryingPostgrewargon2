import sqlite3

def get_Connection():
    conn = sqlite3.connect("Exit_Reasons.db")
    return conn

def createTableOnlyRunOnce():
    conn = get_Connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS deletion_reasons (id INTEGER PRIMARY KEY AUTOINCREMENT,
    reason TEXT NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    conn.commit()
    cursor.close()
    conn.close()

def add_Reason(reason):
    conn = get_Connection()
    cursor = conn.cursor()

    if reason is None:
        reason = "No reason given"

    cursor.execute("INSERT INTO deletion_reasons (reason) VALUES(?)",(reason,))
    conn.commit()
    cursor.close()
    conn.close()


"""if __name__ == "__main__":
    createTableOnlyRunOnce()"""