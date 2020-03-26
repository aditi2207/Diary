import mysql.connector
import datetime
from mysql.connector import Error

conn = None
conn = mysql.connector.connect(host='localhost',
                               database='test',
                               user='root',
                               password='mysql_123',
                               autocommit=True)
cur = conn.cursor()

flag1 = False
flag2 = False


def encyption(pas):
    new_p = ""
    for i in pas:
        x = ord(i)
        x += 1
        x = chr(x)
        new_p += x

    return new_p


def after_login(curr_id, curr_un):
    ch = input("1.Add Note   2.Delete Note   3.Update Note  4.View Notes   5.Search Note  6.Change Username/Password  "
               "7.Filter by date  8.Logout ")
    if ch == '1':
        title = input("Enter title of note: ")
        note = input("Enter note: ")
        cur.execute("INSERT INTO Notes (Id, Date_, Title, Note) values (%s, %s, %s, %s)",
                    (curr_id, datetime.datetime.now(), title, note))
        print("Note added successfully")
        after_login(curr_id, curr_un)

    elif ch == '2':
        val = input("Enter title of note to delete: ")
        cur.execute('DELETE from Notes where Title = "' + val + '";')
        print("Note Successfully deleted!")
        after_login(curr_id, curr_un)

    elif ch == '3':
        val1 = input("Enter title of note to update: ")
        val2 = input("Enter updated note: ")
        cur.execute("Update Notes set note = %s where title = %s", (val2, val1))
        print("Note updated successfully")
        after_login(curr_id, curr_un)

    elif ch == '4':
        print("All notes")
        cur.execute("Select * from Notes where id =" + str(curr_id) + ";")
        print(cur.fetchall())
        after_login(curr_id, curr_un)

    elif ch == '5':
        val = input("Enter title of Note to be searched: ")
        cur.execute('SELECT Title from Notes where Title = "' + val + '";')
        f = cur.fetchall()
        cur.execute('SELECT * FROM Notes where Title = "' + val + '" and Id = "' + str(curr_id) + '"')
        s = cur.fetchall()
        if len(f) == 0:
            print("Note does not exist")
        elif f[0][0] == val:
            print("Found: ")
            print(s)
        after_login(curr_id, curr_un)

    elif ch == '6':
        choice1 = input("1. Change Username   2.Change Password ")
        if choice1 == '1':
            new_un = input("Enter the new username ")
            cur.execute("UPDATE Users set Username = %s where id = %s", (new_un, str(curr_id)))
            print("Username successfully changed")
            after_login(curr_id, curr_un)

        elif choice1 == '2':
            new_pw = input("Enter the new password:")
            cur.execute("UPDATE Users set PW = %s where id = %s", (new_pw, curr_id))
            print("Password successfully changed")
            after_login(curr_id, curr_un)

    elif ch == '7':
        date1 = input("Enter the start date(yyyy-mm-dd): ")
        date2 = input("Enter the end date(yyyy-mm-dd): ")
        cur.execute("SELECT * from Notes WHERE Date_ BETWEEN %s AND %s and id = %s", (date1, date2, str(curr_id)))
        display = cur.fetchall()
        print(display)
        after_login(curr_id, curr_un)

    elif ch == '8':
        log_sign()


def log_sign():
    global flag1, flag2
    print("    DIARY")
    print("1.Login")
    print("2.Don't have an account? Sign-Up")
    choice = input("Enter choice: ")

    if choice == '1':
        usnm = input("Enter username: ")
        pas = input("Enter Password: ")
        cur.execute('select id,PW from Users where Username="' + usnm + '";')
        pw = cur.fetchall()
        check = encyption(pas)
        if len(pw) == 0:
            print("Incorrect Username or Password")
            log_sign()

        elif pw[0][1] == check:
            curr_id = pw[0][0]
            curr_un = usnm
            flag1 = True

    elif choice == '2':
        print("Enter credentials.")
        name = input("Full Name: ")
        email = input("Email address: ")
        phone = input("Contact Number: ")
        addr = input("Address: ")
        age = input("Age: ")
        usnm = input("Enter a username: ")
        pas = input("Enter a password: ")
        pasw = encyption(pas)
        cur.execute("Insert into Users (Full_Name,Email,Contact,Address,Age,Username,PW) values (%s,%s,%s,%s,%s,%s,%s)",
                    (name, email, phone, addr, age, usnm, pasw))
        flag2 = True

    else:
        print("Wrong Choice")
        log_sign()

    if flag1:
        after_login(curr_id, curr_un)

    if flag2:
        log_sign()


def start():
    if conn.is_connected():
        print('Connected to MySQL database')
        log_sign()
    else:
        print('Connection failed.')


start()
