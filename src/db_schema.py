import sqlite3

db = r'..\data\database.db'

def create_urls_table(db):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Urls( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "url" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(req)
        connection.commit()

def create_titles_table(db):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Titles( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "name" TEXT, \
                    "type" TEXT, \
                    "episodes" INTEGER, \
                    "status" TEXT, \
                    "source" TEXT, \
                    "theme" TEXT, \
                    "demographic" TEXT, \
                    "rating" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(req)
        connection.commit()
    
if __name__ == '__main__':
    # create_titles_table(db)
    # create_urls_table(db)
    pass