import requests
from bs4 import BeautifulSoup

top_anime_url = 'https://myanimelist.net/topanime.php'
urls_filepath = r'..\data\urls.csv'

def parse_links_page(url) -> list:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    tr_rows = soup.find_all('tr', class_='ranking-list')
    urls = []
    for row in tr_rows:
        link_tag = row.find('a', class_='hoverinfo_trigger fl-l ml12 mr8')
        urls.append(link_tag.get('href'))

    return urls

def make_urls(pages) -> list:
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

def parse_title_url(title_url) -> dict:
    res = requests.get(title_url)
    soup = BeautifulSoup(res.text, 'lxml')

    keys = (
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

    left_side = soup.find('div', class_='leftside')
    stats = left_side.find_all('div', class_='spaceit_pad')

    res_dict = {}

    name =  soup.find('h1', class_='title-name h1_bold_none').getText()
    
    res_dict['Name'] = [name]

    for stat in stats:
        # good 
        stat_name = stat.find('span').getText()[:-1]

        if stat_name in keys:
            index = keys.index(stat_name)
            res_dict[keys[index]] = []

            links = stat.find_all('a')
            if links:
                for link in links[:-1]:
                    # print(link.get('title'), end=', ')
                    res_dict[keys[index]].append(link.getText())
                # print(links[-1].get('title'))
                res_dict[keys[index]].append(links[-1].getText())
            else:
                # print(stat.getText().split(':')[1].strip())
                res_dict[keys[index]].append(stat.getText().split(':')[1].strip())

    return res_dict

# how name the shit like what studious / genres / bla bla bla are exists ?
def parse_stat_values(stat) -> set:
    stat_values_set = set()
    with open(urls_filepath, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines[1:11]:
            # print(line.split(',')[1][:-1])
            title_info = parse_title_url(line.split(',')[1])
            stat_values_set.add(title_info[stat][0])
    
    return stat_values_set

# studios_values = parse_stat_values('Studios')
# print(studios_values)