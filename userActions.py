from sqliteDBforDeleteReason import add_Reason
from dbcreator import create

def deleteData(name):
    conn = create()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM storeData WHERE username = %s",(name,))
    conn.commit()
    cursor.close()
    conn.close()