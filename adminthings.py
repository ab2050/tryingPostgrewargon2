import dbcreator as dbc
from sqliteDBforDeleteReason import get_Connection

def showData():
    return dbc.show()

def showLogs():
    return dbc.show_logs()

def showDeleteReasons():
    conn = get_Connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM deletion_reasons ORDER BY created_at DESC")
    reasons = cursor.fetchall()
    cursor.close()
    conn.close()
    return reasons