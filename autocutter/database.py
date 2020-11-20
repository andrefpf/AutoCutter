import sqlite3
import pathlib

class DataBase:
    def __init__(self, path):
        self.path = path
        self.conn = self.create_connection()
        self.create_table()
    
    def create_connection(self):
        return sqlite3.connect(self.path)

    def create_table(self):
        if self.table_exists('users'):
            return 
        c = self.conn.cursor()
        c.execute("CREATE TABLE users (id integer, chunk_duration real, threshold real)")

    def table_exists(self, name):
        table_name = (name,)
        c = self.conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ''', table_name)
        return c.fetchone()[0] == 1
    
    def add_user(self, id, chunk_duration, threshold):
        values = (id, chunk_duration, threshold)
        c = self.conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?)", values)
        self.conn.commit()
    
    def remove_user(self, id):
        id = (id,)
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE id = ?", id)
        self.conn.commit()
    
    def remove_all_users(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM users")
        self.conn.commit()
    
    def find_user(self, id):
        id = (id,)
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", id)
        return c.fetchone()
    
    def show(self):
        c = self.conn.cursor()
        for row in c.execute("SELECT * FROM users"):
            print(row)