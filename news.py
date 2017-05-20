import urllib.request
from bs4 import BeautifulSoup

SITE  = urllib.request.urlopen('http://www.latimes.com/').read()
SOUP  = BeautifulSoup(SITE, 'html.parser')

def parse_news_links():
    data = []
    for all_tags in SOUP.find('section', 'trb_outfit').findAll('a'):
        if '.html' in all_tags['href']:
            data.append('http://www.latimes.com' + all_tags['href'])

    return set(data)

def get_tags():
    tags = []
    for all_tags in SOUP.find('ul', 'trb_outfit_group_list').find_all('a', 'trb_outfit_categorySectionHeading_a'):
        tags.append(all_tags.contents[0])
    for all_tags in SOUP.find('ul', 'trb_outfit_list_list').find_all('a', 'trb_outfit_categorySectionHeading_a'):
        tags.append(all_tags.contents[0])

    return(tags)

def combine(news, tags):
    new_data = {}
    # xD
    if 'ESSENTIAL WASHINGTON' in tags:
        tags.pop(tags.index('ESSENTIAL WASHINGTON'))
        tags.append('WASHINGTON')
    for tag in tags:
        for item in news:
            if tag.lower().replace('.', '').replace(' ', '') in item:
                new_data[tag] = item

    return(new_data)

def parse_article(url):
    site  = urllib.request.urlopen(url).read()
    soup  = BeautifulSoup(site, 'html.parser')
    text = ''
    article = soup.find('div', 'trb_ar_page').find_all('p')
    for p in article:
        if p.text not in text and not p.a:
            if 'Credits:' in p.text:
                break
            text += str(p.text + '\n\n')

    return(text)

def parse_photo(url):
    site  = urllib.request.urlopen(url).read()
    soup  = BeautifulSoup(site, 'html.parser')
    img = soup.find('figure', 'trb_embed_imageContainer_figure').find('img')['srcset'].split(' ')
    img = img[len(img) - 2]

    return(img)
