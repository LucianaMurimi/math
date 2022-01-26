import mysql.connector


class DB:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="math_bubbles"
    )
    cursor = db.cursor()

    sql = "INSERT INTO scoreboard (serial_number, score) VALUES (%s, %s)"
    val = (4, 5)
    cursor.execute(sql, val)
    db.commit()

