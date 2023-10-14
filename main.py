import graphene
import psycopg2
import time
import sys
import os
import getpass
from dotenv import load_dotenv

load_dotenv('.env')

print('Loading')

conn = psycopg2.connect(
        host=os.getenv("HOST"),
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT")
        )
cur = conn.cursor()
conn.commit()

print("LOG: DATABASE CONNECTED")

def usernameCheck(usrname):
    cur.execute(f"SELECT * FROM userinfo where username = '{usrname}' LIMIT 1")
    if cur.fetchone():
        return False
    else:
        return True
    
def dbAdd(usrnm,pas):
    length = len(pas)
    if length < 5:
        print("need to be more then 5 chars")
    elif length > 18:
        print("need to be less then 18 chars")
    elif ' ' in pas:
        print("no spaces")
    else:
        retype = getpass.getpass("retype your password: ")
        if pas == retype:
            cur.execute(f"INSERT INTO userinfo (username, password) VALUES('{usrnm}','{pas}');")
            conn.commit()
            print("you may now login")
        elif pas != retype:
            print("passwords dont match")

def login(usrname):
    cur.execute(f"SELECT password FROM userinfo where username = '{usrname}';")
    returne = cur.fetchone()
    if returne == None:
        print("user not found")
    else:
        password = getpass.getpass("password: ")
        if password == returne[0]:
            print(f"Wlecome back,{usrname}")
        else:
            print("password wrong")


wunch = input("LOGIN OR REGISTER [L/R]: ")
wunch = wunch.capitalize()
if wunch == "L":
    username = input("username: ")
    login(username)
elif wunch == "R":
    username = input("username: ")
    if usernameCheck(username) == True:
        print("#your password will not be shown")
        password = getpass.getpass("password:")
        dbAdd(username,password)
    elif usernameCheck(username) == False:
        print("username allready taken")
    
    

cur.close()
conn.close()
