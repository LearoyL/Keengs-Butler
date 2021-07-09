import requests


def dogpic():
    r = requests.get('https://dog.ceo/api/breeds/image/random')
    json_data = r.json()
    url = json_data['message']

    doggie = url

    return doggie
