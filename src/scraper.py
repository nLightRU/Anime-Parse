import requests
import csv
from bs4 import BeautifulSoup

top_anime_url = 'https://myanimelist.net/topanime.php'
urls_filepath = r'..\data\urls.csv'

def parse_links_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tr_rows = soup.find_all('tr', class_='ranking-list')
    urls = []
    for row in tr_rows:
        link_tag = row.find('a', class_='hoverinfo_trigger fl-l ml12 mr8')
        urls.append(link_tag.get('href'))

    return urls

def make_urls(pages):
    urls = []
    for i in range(pages):
        limit = i * 50
        url = 'https://myanimelist.net/topanime.php?limit={x}'.format(x=limit)
        urls.extend(parse_links_page(url))
    return urls

def write_urls_to_csv(csvfile, pages=10):
    urls = make_urls(pages)
    with open(csvfile, 'w', encoding='utf-8') as file:
        file.write('id,url\n')
        id = 0
        for url in urls:
            id += 1
            file.write(str(id) + ',' + url + '\n')

# write_urls_to_csv(links_filepath, 10)

def parse_title_url(title_url):
    res = requests.get(title_url)
    soup = BeautifulSoup(res.text, 'lxml')
    
    left_side = soup.find('div', class_='leftside')
    stats_tags = left_side.find_all('div', class_='spaceit_pad')

    for stat_tag in stats_tags:
        stat_info = stat_tag.getText().split(':')
        stat_name = stat_info[0][1:]
        stat_value = stat_info[1].strip()
        print(stat_name, '->', stat_value)
    
    res_dict = {}
    return res_dict

with open(urls_filepath, encoding='utf-8') as urls_file:
    dict_reader = csv.DictReader(urls_file)
    for row in dict_reader:
        title = parse_title_url(row['url'])
        break