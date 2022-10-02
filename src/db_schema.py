import sqlite3

db = '..\data\database.db'

def create_urls_table(db):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Urls( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "url" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(req)
        connection.commit()

