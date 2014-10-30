import sqlite3 as db

def initial_database():
    conn = db.connect('gameRecom.db')
    c = conn.cursor()
    c.execute()
