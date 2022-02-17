import mysql.connector
import bcrypt
from globals import *

class DB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="math_bubbles"
        )
        self.cursor = self.db.cursor()

    def SignIn(self, email, passwd):
        # sql = "INSERT INTO scoreboard (serial_number, score) VALUES (%s, %s)"
        # val = (4, 5)
        # cursor.execute(sql, val)
        # db.commit()
        email_split = email.split('_')
        print(email_split)

        sql = "SELECT * FROM users WHERE email = %s"
        email_address = (email_split[0] + "@gmail.com",)

        print(email_address)
        self.cursor.execute(sql, email_address)

        result = self.cursor.fetchone()
        passwdHashed = result[4]

        if bcrypt.checkpw(passwd.encode('utf-8'), passwdHashed.encode('utf-8')):
            print("True")
            global TABLENAME
            TABLENAME = email
            return result
        else:
            print("False")
            return False

    def upload(self, level_1=0, level_2=0):
        sql = "INSERT INTO "+TABLENAME+" (level_1, level_2) VALUES (%s, %s)"
        print("1", LEVEL1_SCORE)
        scores = (level_1, level_2)
        self.cursor.execute(sql, scores)
        self.db.commit()


