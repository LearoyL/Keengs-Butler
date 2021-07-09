import json
import urllib.request


def catapi():
    url = "https://api.thecatapi.com/v1/images/search"
    header = {'X-ApiKey': '34cf45f5-c025-43d8-ba10-beb7e0bf8674'}
    req = urllib.request.Request(url, None, header)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return data[0].get('url')
