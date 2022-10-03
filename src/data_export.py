import csv
import json
import sqlite3

urls = r'..\data\urls.csv'
db = r'..\data\database.db'
titles = r'..\data\titles.json'

def export_urls_to_db(urls_filepath, database):
    with sqlite3.connect(database) as connection, open(urls_filepath, encoding='utf-8') as file:
        cursor = connection.cursor()
        dict_reader = csv.DictReader(file)
        
        for row in dict_reader:
            cursor.execute('INSERT INTO Urls(url) VALUES("{x}")'.format(x=row['url']))
        
        connection.commit()

def export_titles_to_db(titles, database):
    with sqlite3.connect(database)      as con, \
         open(titles, encoding='utf-8') as f:

        cur = con.cursor()
        
        for line in f:
            data = json.loads(line)
            
            if data['episodes'] == 'Unknown':
                data['episodes'] = '0'

            values_tuple = ( 
                data['name'],
                data['type'],
                int(data['episodes']),
                data['status'],
                int(data['year']),
                data['source'],
                data['theme'],
                data['demographic'],
                data['rating']
            )

            cur.execute('INSERT INTO Titles(name, \
                                            type, \
                                            episodes, \
                                            status, \
                                            year, \
                                            source, \
                                            theme, \
                                            demographic, \
                                            rating) \
                        VALUES (?,?,?,?,?,?,?,?,?)', 
                        values_tuple)

        con.commit()

def filter_uniques(src_f, key: str) -> set:
    result = set()

    with open(src_f, encoding='utf-8') as src:
        for line in src:
            data = json.loads(line)

            if type(data[key]) == list:
                for val in data[key]:
                    result.add(val)
            else:
                result.add(data[key])

    return result

def write_uniques_to_file(uniques, fp):
    with open(fp, 'w', encoding='utf-8') as f:
        for val in uniques:
            f.write(val + '\n')

def export_studios_to_db(studios, db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for val in studios:
            cur.execute('INSERT INTO Studios(name) VALUES(?)',(val,))
        con.commit()

def export_genres_to_db(genres, db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for val in genres:
            cur.execute('INSERT INTO Genres(name) VALUES(?)',(val,))
        con.commit()


__keys__ = (
            'name',
            'type', 
            'episodes',
            'status',
            'source',
            'theme',
            'demographic',
            'rating'
        )

if __name__ == '__main__':
    # studios = filter_uniques(titles, 'studios')
    # genres = filter_uniques(titles, 'genres')
    # for val in genres:
    #     print(val)

    # write_uniques_to_file(studios, r'..\data\studios.txt')
    # write_uniques_to_file(genres, r'..\data\genres.txt')

    # for val in ratings:
    #     print(val)

    # export_urls_to_db(urls, db)
    # export_titles_to_db(titles, db)
    # export_studios_to_db(studios, db)
    # export_genres_to_db(genres, db)