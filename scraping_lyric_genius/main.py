from collections import Counter
from pprint import pprint
from bs4 import BeautifulSoup
import requests


#Enter number Artiste API
artiste_number = int(input("Enter number Artiste API: "))

#Enter length of worls in lyrics
world_lenght= int(input('Enter length of worlds in lyrics: '))

def is_valid(word):
    if len(word) <  world_lenght:
        return False
    if "[" in word and "]" in word:
        return False
    return True


def extract_lyrics(url):
    print(f'fetching lyrics ... {url}')
    r = requests.get(url)

    if r.status_code != 200:
        print('Mauvaise url')
        return []

    soup = BeautifulSoup(r.content, 'html.parser')
    lyrics = soup.find_all("div", class_='Lyrics__Container-sc-1ynbvzw-10')

    if not lyrics:
        return extract_lyrics(url)

    all_words = []
    for sentence in lyrics:
        paroles = sentence.stripped_strings
        for parole in paroles:
            sentence_words = [word.strip(',').strip('.').lower() for word in parole.split() if is_valid(word)]
            all_words.extend(sentence_words)
    return all_words

######On recupere les url des chanson######
def get_all_urls():
    links = []
    page_number = 1
    while True:
        r = requests.get(f'https://genius.com/api/artists/{artiste_number}/songs?page={page_number}&per_page=10')
        print(f'fetching page {page_number}')
        if r.status_code == 200:
            response = r.json().get('response',{})
            next_page = response.get('next_page')
            songs = response.get('songs')

            all_songs_links = [song.get('url') for song in songs]
            links.extend(all_songs_links)

            page_number += 1

            if not next_page:
                print('No more pages to fetch...')
                break
    return links

def get_all_words():
    urls = get_all_urls()
    words = []
    for url in urls[:10]:
        lyrics = extract_lyrics(url=url)
        words.extend(lyrics)
    counter = Counter(words)
    most_common_words = counter.most_common(10)
    pprint(most_common_words)

get_all_words()
