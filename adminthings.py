import dbcreator as dbc

def showrecords():
    s = input("do you wanna see the whole table ? (y/n)")
    if s == "y":
        dbc.show()

    else:
        s = input("Wanna see logs ? y/n")
        if s=="y":
            dbc.show_logs()
        else:    
            print(":]")