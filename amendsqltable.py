#only to be run once, adds date of joining
import dbcreator as dbc

conn = dbc.create()
cursor = conn.cursor()

#cursor.execute("ALTER TABLE storeData ADD COLUMN join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
#conn.commit()

cursor.execute("UPDATE storeData SET join_date = CURRENT_TIMESTAMP WHERE join_date IS NOT NULL;")
conn.commit()

#cursor.execute("ALTER TABLE storeData ADD COLUMN exit_date TIMESTAMP")
#conn.commit()