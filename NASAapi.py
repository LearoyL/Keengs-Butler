import requests


def nasapic():
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key=p1zFjT1gmWhQ1fg6bUQhdmqoY4APqEsgigovlYjX')
    json_data = r.json()
    explain = json_data['explanation']
    url = ['hdurl']
    title = ['tittle']
    nasa = ('**' + str(title) + '**\n'
                                '*' + str(explain) + '*\n'
            + url)
    return nasa

# {'copyright': 'Miguel Claro',
# 'date': '2021-06-25',
# 'explanation':
# 'hdurl':
# 'media_type': 'image',
# 'service_version': 'v1',
# 'title': 'Andromeda in a Single Shot',
# 'url': 'https://apod.nasa.gov/apod/image/2106/AndromedaGalaxy-SingleShotMina-4688-net1200.jpg'}
