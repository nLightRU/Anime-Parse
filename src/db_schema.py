import sqlite3
import json

db = r'..\data\database.db'

titles = r'..\data\titles.json'

titles_first = r'..\data\titles_first.json'
titles_second = r'..\data\titles_second.json'

def create_urls_table(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Urls( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "url" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cur.execute(req)
        con.commit()

def create_titles_table(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
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
        cur.execute(req)
        con.commit()

def create_studios_table(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Studios( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "name" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cur.execute(req)
        con.commit()

def create_genres_table(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        req = 'CREATE TABLE IF NOT EXISTS Genres( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "name" TEXT, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cur.execute(req)
        con.commit()

def create_titles_genres_table(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        req = req = 'CREATE TABLE IF NOT EXISTS TitlesGenres( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "id_title" INTEGER, \
                    "id_genre" INTEGER, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cur.execute(req)
        con.commit()

def fill_titles_genres(db, titles):
    with sqlite3.connect(db) as con, open(titles, encoding='utf-8') as f:
        cur = con.cursor()

        rows = cur.execute('SELECT id, name FROM Genres')
        genres_dict = {}
        for row in rows:
            genres_dict[row[1]] = row[0]
            
        title_names = list(cur.execute('SELECT id, name FROM Titles'))

        for title_line in f.readlines():
            title = json.loads(title_line)

            for row in title_names:
                if row[1] == title['name']:
                    title_id = row[0]

            print(title['name'], title_id)

            genres = title['genres']
            if type(genres) == list:
                for genre in genres:
                    genre_id = genres_dict[genre]
                    cur.execute('INSERT INTO TitlesGenres(id_title, id_genre) VALUES(?, ?)', (title_id, genre_id))
            else:
                genre_id = genres_dict[genres]
                cur.execute('INSERT INTO TitlesGenres(id_title, id_genre) VALUES(?, ?)', (title_id, genre_id))

            con.commit()

def create_titles_studios_table(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        req = req = 'CREATE TABLE IF NOT EXISTS TitlesStudios( \
                    "id" INTEGER NOT NULL UNIQUE, \
                    "id_title" INTEGER, \
                    "id_studio" INTEGER, \
                    PRIMARY KEY("id" AUTOINCREMENT))'
        cur.execute(req)
        con.commit()

def fill_titles_studios(db, titles):
    with sqlite3.connect(db) as con, open(titles, encoding='utf-8') as f:
        cur = con.cursor()

        rows = cur.execute('SELECT id, name FROM Studios')
        studios_dict = {}
        for row in rows:
            studios_dict[row[1]] = row[0]
            
        title_names = list(cur.execute('SELECT id, name FROM Titles'))

        for title_line in f.readlines():
            title = json.loads(title_line)

            for row in title_names:
                if row[1] == title['name']:
                    title_id = row[0]

            print(title['name'], title_id)

            studios = title['studios']
            if type(studios) == list:
                for studio in studios:
                    studo_id = studios_dict[studio]
                    cur.execute('INSERT INTO TitlesStudios(id_title, id_studio) VALUES(?, ?)', (title_id, studo_id))
            else:
                studo_id = studios_dict[studios]
                cur.execute('INSERT INTO TitlesStudios(id_title, id_studio) VALUES(?, ?)', (title_id, studo_id))

            con.commit()

def create_database():
    create_urls_table(db)
    create_titles_table(db)
    create_studios_table(db)
    create_genres_table(db)

    create_titles_genres_table(db)
    create_titles_studios_table(db)

if __name__ == '__main__':
    pass