#!/usr/bin/env python3
import re
import news
import vk_post
from sys import stdout
from collections import Counter
from time import sleep, strftime, time

def common_words(text):
    words = re.findall(r'\w+', text)
    cap_words = [word for word in words if len(word) >= 8]
    word_counts = Counter(cap_words)

    common = []

    for key in dict(word_counts):
        if  word_counts[key] > 4:
            common.append(key.title())

    return(common)

def print_status(status):
    stdout.write("\n[{0}] > {1}".format(strftime('%H:%M:%S'), status))

def post_news(link, write_old):
    articles = news.combine(link, news.get_tags())

    for value in articles:
        try:
            print_status('Posting news...')

            parsed_text = news.parse_article(articles[value]).replace('ALSO', '')
            hashtags = '#News #LosAngeles #LATimes #{0} '.format(value.lower().replace('.', '').replace(' ', '').title())
            common = common_words(parsed_text)
            if common:
                for word in common:
                    hashtags += '#{0} '.format(word)
            parsed_text += hashtags
            photo_link = news.parse_photo(articles[value])
            photo = vk_post.wallPhoto(photo_link)
            if vk_post.make_post(parsed_text, photo, articles[value]):
                write_old.write(articles[value] + '\n')
            else:
                write_old.write(articles[value] + '\n')

            print_status('News were posted...')

        except KeyError:
            write_old.write(articles[value] + '\n')

def update_news():
    try:
        posted_links = []
        ready_to_post = []

        base = open('/mnt/0/Download/latimes/latimes/posted_links.txt', 'r+')

        print('Base ready\n')
        for link in base:
            posted_links.append(link.rstrip().split('#')[0])

        get_news = news.parse_news_links()

        for link in get_news:
            if link.split('#')[0] not in posted_links:

                ready_to_post.append(link.split('#')[0])

        if ready_to_post:
            post_news(ready_to_post, base)
        
    except AttributeError:
        pass

if __name__ == '__main__':
    update_news()
