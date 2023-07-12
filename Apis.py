import json
import random
import NSFWlist
import urllib.request

from datetime import datetime

import requests


# noinspection DuplicatedCode
def hackkeengs():  # MY bread and butter function
    r = requests.get('https://mtxserv.com/api/v1/viewers/game?type=minecraft&ip=game-fr-43.mtxserv.com&port=27280')

    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt2 = str(dt_string)
    lastupdate = "**Last Update**  = " + ' ' + dt_string + ''

    json_data = r.json()
    is_online = json_data['is_online']
    # ip = json_data ['ip']
    # host_name = json_data ['params']['host_name']
    # joinlink = json_data ['params']['joinlink']
    # max_slots = json_data['params']['max_slots']
    # players = json_data['params']['players']
    # print(json_data)

    # if server is online or offine - serveronoff

    if is_online:
        serveronoff = 'Server Online'
        max_slots = json_data['params']['max_slots']
        players = json_data['params']['players']
        playernumber = len(players)
        names = '**Connected Players: **'
        if playernumber > 0:
            for player in players:
                names += player['player'] + ' **-** '
            names = names[:-7]
        else:
            names = '**No one is on , sadge....**'
        x = ('...HACKING SERVER...\n'
             '' + serveronoff + '\n'
                                '**Server-IP: ** 51.255.235.102:27280\n'
                                '**Online Player**: ' + str(playernumber) + '/' + str(max_slots) + '\n'
                                                                                                   '' + names + '\n'
                                                                                                                '' + lastupdate + ' **UTC +3**')
        serverlsit = [serveronoff, playernumber, max_slots, names, lastupdate]
    else:
        serveronoff = 'SERVER IS DEAD @LEAROY ASAP SAVE IT NOW'
        playernumber = 0
        max_slots = 'null'
        names = 'null'
        x = ('...HACKING SERVER...\n'
             '' + serveronoff + '\n'
                                '**Server-IP: ** 51.255.235.102:27280\n'
                                '**Online Player**: ' + '0' + '/' + '40' + '\n'
                                                                           '' + lastupdate + ' **UTC +3**')
        serverlsit = [serveronoff, playernumber, max_slots, names, dt2]

    return serverlsit


# Coin Flipper
def coin():
    range = [1, 2]
    r = random.randrange(0, len(range))
    flip = range[r]
    if flip == 1:
        res = 'Heads'
    else:
        res = 'Tails'
    return res


# WORD API
def randomword():
    wordnumber = 1
    r = requests.get('https://random-word-api.herokuapp.com/word?number=' + str(wordnumber) + '')
    json_data = r.json()
    word1 = json_data[0]
    return word1


# INSULT API
def insult():
    r = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
    json_data = r.json()
    ins = json_data['insult']
    return ins


# MEME API
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
    #
    # submeme = ('**' + title + '**\n'
    #            + url)
    memedict = {'title': title, 'url': url}
    return memedict


# DOG API
def dogpic():
    r = requests.get('https://dog.ceo/api/breeds/image/random')
    json_data = r.json()
    url = json_data['message']

    doggie = url

    return doggie


# CAT API
def catapi():
    url = "https://api.thecatapi.com/v1/images/search"
    header = {'X-ApiKey': '34cf45f5-c025-43d8-ba10-beb7e0bf8674'}
    req = urllib.request.Request(url, None, header)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return data[0].get('url')


# NSFW API
def booba():
    cat = NSFWlist.doggy
    randomnum = random.randrange(0, len(cat))
    r = requests.get('https://meme-api.herokuapp.com/gimme/' + cat[randomnum])
    json_data = r.json()
    title = json_data['title']
    url = json_data['url']

    porn = ('**' + title + '**\n'
            + url)

    return porn


# NASA API
def nasapic():
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key=p1zFjT1gmWhQ1fg6bUQhdmqoY4APqEsgigovlYjX')
    json_data = r.json()
    explain = json_data['explanation']
    url = ['hdurl']
    title = ['tittle']
    nasa = ('**' + str(title) + '**\n'
                                '*' + str(explain) + '*\n'
            + str(url))
    return nasa


# JOKE API
def joke():
    r = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=racist,sexist&type=single')
    json_data = r.json()
    # cat = json_data['category']
    return_joke = json_data['joke']
    return return_joke


# Comliement API
def Compliment():
    r = requests.get('https://complimentr.com/api')
    json_data = r.json()
    comp = json_data['compliment']
    return comp


a = '🇦'
b = '🇧'
c = '🇨'
d = '🇩'
e = '🇪'
f = '🇫'
g = '🇬'
h = '🇭'
i = '🇮'
j = '🇯'
k = '🇰'
l = '🇱'
m = '🇲'
n = '🇳'
o = '🇴'
p = '🇵'
q = '🇶'
r = '🇷'
s = '🇸'
t = '🇹'
u = '🇺'
v = '🇻'
w = '🇼'
x = '🇽'
y = '🇾'
z = '🇿'

letterdict = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i, 'j': j, 'k': k, 'l': l, 'm': m,
              'n': n, 'o': o, 'p': p, 'q': q, 'r': r, 's': s, 't': t, 'u': u, 'v': v, 'w': w, 'x': x, 'y': y, 'z': z}
