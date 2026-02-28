import mysql.connector as sql
from random import randint

print("Enter the details of your MySQL Server:")
x = input("Hostname: ")
y = input("User: ")
z = input("Password: ")

con = sql.connect(host=x, user=y, password=z)
con.autocommit = True
cur = con.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS IRCTC;")
cur.execute("USE IRCTC;")

cur.execute("""
CREATE TABLE IF NOT EXISTS accounts(
id int primary key,
pass varchar(16),
name varchar(100),
sex char(1),
age varchar(3),
dob date,
ph_no char(10));
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tickets(
id int,
PNR int,
train varchar(25),
doj date,
tfr varchar(100),
tto varchar(100));
""")

# ---------------- LOGIN MENU ----------------

def login_menu():
    print("《"*23, "WELCOME TO THE IRCTC PORTAL", "》"*23)
    print("1. Create New Account")
    print("2. Log In")
    print("3. Exit\n")

    opt = int(input("Enter your choice: "))

    if opt == 1:
        create_acc()
    elif opt == 2:
        login()
    else:
        e = input("Exit the portal? (Y/N) ")
        if e in "Nn":
            login_menu()

# ---------------- CREATE ACCOUNT ----------------

def create_acc():
    print("Enter the details to create your account:")

    i = randint(1000, 10000)
    print(f"Your generated ID is: {i}")

    p = input("Enter your password: ")
    n = input("Enter your name: ")
    sex = input("Enter your gender (M/F/O): ")
    age = input("Enter your age: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    ph = input("Enter your contact number: ")

    cur.execute(
        "INSERT INTO accounts VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (i, p, n, sex.upper(), age, dob, ph)
    )

    print("Account created successfully!\n")
    login()

# ---------------- LOGIN ----------------

def login():
    global a
    try:
        a = int(input("Enter your ID: "))
        b = input("Enter your password: ")

        cur.execute(
            "SELECT name FROM accounts WHERE id=%s AND pass=%s",
            (a, b)
        )

        j = cur.fetchone()

        if j:
            print(f"Welcome back {j[0]}!\n")
            main_menu()
        else:
            raise Exception

    except:
        print("Your account was not found!")
        print("1. Try logging in again")
        print("2. Create a new account\n")

        ch = input("Enter your choice: ")

        if ch == "1":
            login()
        elif ch == "2":
            create_acc()
        else:
            login_menu()

# ---------------- MAIN MENU ----------------

def main_menu():
    print("What would you like to do today?")
    print("1. Purchase a Ticket")
    print("2. Check Ticket Status")
    print("3. Request a refund")
    print("4. Account Settings")
    print("5. Logout")
    print("6. Exit\n")

    ch1 = int(input("Enter your choice: "))

    if ch1 == 1:
        buy_ticket()
    elif ch1 == 2:
        show_ticket()
    elif ch1 == 3:
        cancel_ticket()
    elif ch1 == 4:
        account()
    elif ch1 == 5:
        login_menu()
    else:
        exit()

# ---------------- BUY TICKET ----------------

def buy_ticket():
    print("Enter details for your journey:\n")

    pnr = randint(100000, 1000000)
    print(f"Your PNR is {pnr}")

    train = input("Enter the name of the train: ")
    doj = input("Enter the date (YYYY-MM-DD): ")
    fr = input("Enter Departing Station: ")
    to = input("Enter Destination Station: ")

    cur.execute(
        "INSERT INTO tickets VALUES (%s,%s,%s,%s,%s,%s)",
        (a, pnr, train, doj, fr, to)
    )

    print("Ticket booked successfully!\n")
    main_menu()

# ---------------- SHOW TICKET ----------------

def show_ticket():
    pnr = int(input("Enter your PNR: "))

    cur.execute("SELECT * FROM tickets WHERE pnr=%s", (pnr,))
    j = cur.fetchone()

    if j and j[0] == a:
        print(f"Train: {j[2]}")
        print(f"Date: {j[3]}")
        print(f"From: {j[4]}")
        print(f"To: {j[5]}\n")
    else:
        print("Ticket not found or Unauthorized!\n")

    main_menu()

# ---------------- CANCEL TICKET ----------------

def cancel_ticket():
    pnr = int(input("Enter PNR number: "))

    cur.execute("SELECT id FROM tickets WHERE pnr=%s", (pnr,))
    j = cur.fetchone()

    if j and j[0] == a:
        cur.execute("DELETE FROM tickets WHERE pnr=%s", (pnr,))
        print("Ticket cancelled. Refund will be processed.\n")
    else:
        print("Unauthorized or ticket not found!\n")

    main_menu()

# ---------------- ACCOUNT ----------------

def account():
    print("1. Show Account details")
    print("2. Delete Account\n")

    ch = int(input("Enter your choice: "))

    if ch == 1:
        cur.execute("SELECT * FROM accounts WHERE id=%s", (a,))
        j = cur.fetchone()

        if j:
            print(f"ID: {j[0]}")
            print(f"Name: {j[2]}")
            print(f"Gender: {j[3]}")
            print(f"Age: {j[4]}")
            print(f"DOB: {j[5]}")
            print(f"Phone: {j[6]}\n")

        main_menu()

    elif ch == 2:
        cur.execute("DELETE FROM tickets WHERE id=%s", (a,))
        cur.execute("DELETE FROM accounts WHERE id=%s", (a,))
        print("Account deleted successfully!\n")
        login_menu()

# ---------------- START PROGRAM ----------------

if __name__ == "__main__":
    login_menu()