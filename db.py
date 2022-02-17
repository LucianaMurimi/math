import mysql.connector
import bcrypt

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

        sql = "SELECT * FROM users WHERE email = %s"
        email_address = (email + "@gmail.com",)

        self.cursor.execute(sql, email_address)

        result = self.cursor.fetchone()
        passwdHashed = result[4]

        if bcrypt.checkpw(passwd.encode('utf-8'), passwdHashed.encode('utf-8')):
            print("True")
            return result
        else:
            print("False")
            return False


