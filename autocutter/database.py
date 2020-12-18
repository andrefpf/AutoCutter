import sqlite3
import pathlib

class DataBase:
    def __init__(self, path):
        self.path = path
        self.create_table()
    
    def create_table(self):
        if self.table_exists('users'):
            return 
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE users (id integer, chunk_duration real, threshold real)")

    def table_exists(self, name):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ''', (name,))
            return c.fetchone()[0] == 1

    def add_user(self, id, chunk_duration, threshold):
        with sqlite3.connect(self.path) as conn:
            values = (id, chunk_duration, threshold)
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES (?,?,?)", values)
            conn.commit()

    def remove_user(self, id):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
    
    def update_chunk(self, id, chunk_duration):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET chunk_duration = ? WHERE id = ?", (chunk_duration, id))
            conn.commit()
    
    def update_threshold(self, id, threshold):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET threshold = ? WHERE id = ?", (threshold, id))
            conn.commit()
    
    def remove_all_users(self):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users")
            conn.commit()
    
    def find_user(self, id):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id = ?", (id,))
            return c.fetchone()
    
    def show(self):
        with sqlite3.connect(self.path) as conn:
            for row in conn.cursor().execute("SELECT * FROM users"):
                print(row)