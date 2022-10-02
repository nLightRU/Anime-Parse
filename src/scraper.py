import csv
import requests
from bs4 import BeautifulSoup

top_anime_url = 'https://myanimelist.net/topanime.php'
urls_filepath = r'..\data\urls.csv'

__keys__ = (
            'Name',
            'Type', 
            'Episodes',
            'Status',
            'Studios',
            'Source',
            'Genres',
            'Theme',
            'Demographic',
            'Rating'
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
    
    res_dict['Name'] = [name]

    for stat in stats:
        # good 
        stat_name = stat.find('span').getText()[:-1]

        if stat_name in __keys__:
            index = __keys__.index(stat_name)
            res_dict[__keys__[index]] = []

            links = stat.find_all('a')
            if links:
                for link in links[:-1]:
                    # print(link.get('title'), end=', ')
                    res_dict[__keys__[index]].append(link.getText())
                # print(links[-1].get('title'))
                res_dict[__keys__[index]].append(links[-1].getText())
            else:
                # print(stat.getText().split(':')[1].strip())
                res_dict[__keys__[index]].append(stat.getText().split(':')[1].strip())

    return res_dict
    

# how name the shit like what studious / genres / bla bla bla are exists ?
# we get it from csv with titles
# def create_stat_values(stat) -> set:
#     stat_values_set = set()
#     with open(urls_filepath, encoding='utf-8') as file:
#         lines = file.readlines()
#         for line in lines[1:11]:
#             # print(line.split(',')[1][:-1])
#             title_info = parse_title_url(line.split(',')[1])
#             stat_values_set.add(title_info[stat][0])
    
#     return stat_values_set

if __name__ == '__main__':
    # urls = make_urls(10)
    # write_urls_to_csv(urls, urls_filepath)
    with open(urls_filepath, 'r', encoding='utf-8') as urls_f:
        dict_reader = csv.DictReader(urls_f)
        for title in dict_reader:
            title_url = title['url']
            res = parse_title(title_url)
            for key in res:
                print(key, res[key])
            break