import csv
import sqlite3

urls = r'..\data\urls.csv'
db = r'..\data\database.db'

def export_urls(db, urls_filepath):
    with sqlite3.connect(db) as connection, open(urls_filepath, encoding='utf-8') as file:
        cursor = connection.cursor()
        dict_reader = csv.DictReader(file)
        
        for row in dict_reader:
            cursor.execute('INSERT INTO Urls(url) VALUES("{x}")'.format(x=row['url']))
        
        connection.commit()
