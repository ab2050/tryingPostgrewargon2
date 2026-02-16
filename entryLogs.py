import logging

successlog = logging.getLogger("successlog")
successlog.setLevel(logging.INFO)#check moodle for setlevel info details

successfile = logging.FileHandler("Successful_Logins.log")
format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")#check moodle for format details
successfile.setFormatter(format)
successlog.addHandler(successfile)

faillog = logging.getLogger("faillog")
faillog.setLevel(logging.INFO)

failfile = logging.FileHandler("Failed_Logins.log")
failfile.setFormatter(format)
faillog.addHandler(failfile)