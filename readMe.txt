GDPR ALLOWS STORAGE OF IP ADDRESSES BUT ONLY WITH PROPER REASON, INFORMED CONSENT AND WITH PROPER SECURITY ONLY. REMOVE IP FROM LOGS OR CREATE NEW LOG FILES INSTEAD.

Main task : Store data in postgre, 2 user roles - user or admin, admin can see logs and all records
Failed login attempts get stored in login_logs table
User records are stored in storeData table

Files :
mainpage.py : asks for existing user or new, sends to login.py or register.py

register.py : takes name and password, sends password to passwordAuth.py, gets the hash and calls
dbCreator's make function to create a new user

login.py : Asks for name, password and role, verifies name, if name is present, gets password has,
calls passwordAuth.py to verify. If verified and user is an admin, asks user if they want to do any
admin work, and calls adminthings.py

adminthings.py : Allows admins to check all records, or check login_logs by calling dbCreator.py's
show and show logs function

passwordAuth.py : Uses argon2.passwordHasher, to hash new passwords and also verify user logins

dbCreator.py : All SQL functions are done here, creates and returns the connection. Has maketables to create tables
Make() to add new users
Show() to show all users
Show_logs() to show login_logs
