import requests
from bs4 import BeautifulSoup

top_anime_url = 'https://myanimelist.net/topanime.php'

def parse_links(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tr_rows = soup.find_all('tr', class_='ranking-list')
    links = []
    for row in tr_rows:
        link_tag = row.find('a', class_='hoverinfo_trigger fl-l ml12 mr8')
        links.append(link_tag.get('href'))

    return links

def make_links(pages):
    links = []
    for i in range(pages):
        limit = i * 50
        url = 'https://myanimelist.net/topanime.php?limit={x}'.format(x=limit)
        links.extend(parse_links(url))
    return links

def write_links_to_csv(csvfile, pages=10):
    links = make_links(pages)
    with open(csvfile, 'w', encoding='utf-8') as file:
        file.write('id,link\n')
        id = 0
        for link in links:
            id += 1
            file.write(str(id) + ',' + link + '\n')

links_filepath = '..\data\links.csv'

write_links_to_csv(links_filepath, 10)

