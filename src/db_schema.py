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
                    "year" INTGER, \
                    "source" TEXT, \
                    "theme" TEXT, \
                    "demographic" TEXT, \
                    "rating" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(req)
        connection.commit()

def create_studios_table(db):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Studios( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "name" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(req)
        connection.commit()

def create_genres_table(db):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Genres( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "name" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cursor.execute(req)
        connection.commit()

if __name__ == '__main__':
    # create_urls_table(db)
    # create_titles_table(db)
    # create_studios_table(db)
    # create_genres_table(db)
    pass