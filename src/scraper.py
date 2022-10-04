import csv
import requests
import json
from bs4 import BeautifulSoup

top_anime_url = 'https://myanimelist.net/topanime.php'
urls_filepath = r'..\data\urls.csv'
titles_filepath = r'..\data\titles.json'

titles_first = r'..\data\titles_first.json'
titles_second = r'..\data\titles_second.json'

__keys__ = (
            'name',
            'type', 
            'episodes',
            'status',
            'year',
            'studios',
            'source',
            'genres',
            'theme',
            'demographic',
            'rating'
        )

def get_urls_from_page(url) -> list:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tr_rows = soup.find_all('tr', class_='ranking-list')
    urls = []
    for row in tr_rows:
        link_tag = row.find('a', class_='hoverinfo_trigger fl-l ml12 mr8')
        urls.append(link_tag.get('href'))

    return urls

def make_urls(pages=10) -> list:
    urls = []
    for i in range(pages):
        limit = i * 50
        req = 'https://myanimelist.net/topanime.php?limit={x}'.format(x=limit)
        urls_from_page = get_urls_from_page(req)
        urls.extend(urls_from_page)
    return urls

def write_urls_to_csv(urls, csvfile, pages=10):
    with open(csvfile, 'w', newline = '', encoding='utf-8') as f:
        header = 'id,url\n'
        f.write(header)
        for id, url in enumerate(urls, start=1):
            f.write(str(id) + ',' + url + '\n')

def parse_title(url) -> dict:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    left_side = soup.find('div', class_='leftside')
    stats = left_side.find_all('div', class_='spaceit_pad')

    res_dict = {}

    name =  soup.find('h1', class_='title-name h1_bold_none').getText()
    
    res_dict['name'] = name

    for stat in stats:
        # good 
        stat_name = stat.find('span').getText()[:-1]

        stat_name = stat_name.lower()

        if stat_name == 'aired':
            year = stat.getText().strip()
            year = year.split(':')[1]
            year = year.split(' ')[4]
            # year = year.split(' ')
            res_dict['year'] = year

        if stat_name == 'genre':
            link = stat.find('a')
            res_dict['genres'] = link.getText()

        if stat_name in __keys__:
            res_dict[stat_name] = []

            links = stat.find_all('a')
            if links:
                for link in links[:-1]:
                    # print(link.get('title'), end=', ')
                    res_dict[stat_name].append(link.getText())
                # print(links[-1].get('title'))
                res_dict[stat_name].append(links[-1].getText())
            else:
                # print(stat.getText().split(':')[1].strip())
                res_dict[stat_name] = stat.getText().split(':')[1].strip()
            
            if len(res_dict[stat_name]) == 1:
                res_dict[stat_name] = res_dict[stat_name][0]
    
    for key in __keys__:
        if key not in res_dict.keys():
            res_dict[key] = 'Undefined'

    return res_dict

def parse_titles(urls, start: int=1, end:int=10) -> list:
    titles = []
    with open(urls, encoding='utf-8') as f:
        for line in f.readlines()[start:end + 1]:
            url = line.split(',')[1]
            print(line.split(',')[0])
            titles.append(parse_title(url))
    return titles

def write_title_to_json(title_dict: dict, json_file) -> None:
    with open(json_file, 'a', encoding='utf-8') as f:
        title_str = json.dumps(title_dict)
        f.write(title_str + '\n')    

if __name__ == '__main__':
    pass
