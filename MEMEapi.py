import random

import requests


def subbreddit():
    doomisnotcool = [
        'me_irl',
        'memes',
        'dankmemes',
        'shittyreactiongifs'

    ]
    randomnum = random.randrange(0, len(doomisnotcool))
    r = requests.get('https://meme-api.herokuapp.com/gimme/' + doomisnotcool[randomnum])
    # print(randomnum)
    json_data = r.json()
    title = json_data['title']
    url = json_data['url']

    submeme = ('**' + title + '**\n'
               + url)
    memedict = {'title': title, 'url':url}
    return memedict
