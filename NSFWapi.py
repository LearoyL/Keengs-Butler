import requests
import random


def booba():
    cat = [
        'NSFW',
        'Hentai',
        'rule34'
    ]
    randomnum = random.randrange(0, len(cat))
    r = requests.get('https://meme-api.herokuapp.com/gimme/' + cat[randomnum])
    json_data = r.json()
    title = json_data['title']
    url = json_data['url']

    pron = ('**' + title + '**\n'
            + url)

    return pron
