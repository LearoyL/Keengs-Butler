import random

import requests


def valagent():
    # Get random number exculding 5
    numbers = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    ragent = random.choice(numbers)
    # print(ragent)
    r = requests.get('https://valorant-api.com/v1/agents')
    json_data = r.json()
    name = json_data['data'][ragent]['displayName']
    pic = json_data['data'][ragent]['bustPortrait']
    desc = json_data['data'][ragent]['description']
    role = json_data['data'][ragent]['role']['displayName']
    icon = json_data['data'][ragent]['role']['displayIcon']
    eagent = ('**' + name + '**\n'
              + pic)
    valdict = {'name': name, 'pic': pic, 'desc': desc, 'role': role, 'icon': icon}
    return valdict


def valcomp():
    # Grabbing a map splash
    rmap = random.randrange(0,6)
    r = requests.get('https://valorant-api.com/v1/maps')
    json_data = r.json()
    splash = json_data['data'][rmap]['splash']
    # 1 Sentinels - 1 Controller - 2 Duelist - 1 Initiators
    # 2 Sentinels - 1 Controller - 1 Duelist - 1 Initiators
    # 0 Sentinels - 2 Controller - 1 Duelist - 2 Initiators
    # 1 Sentinels - 0 Controller - 2 Duelist - 2 Initiators
    comps = {1: '1-1-2-1', 2: '2-1-1-1', 3: '0-2-1-2', 4: '1-0-2-2'}
    # Lists of agents
    sentinels = ['Sage', 'Cypher', 'Killjoy']
    controllers = ['Astra', 'Brimstone', 'Omen', 'Viper']
    duelist = ['Jett', 'Phoenix', 'Raze', 'Reyna', 'Yoru']
    initiators = ['Sova', 'Skye', 'Breach', 'Kay/o', 'Sova', 'Skye']
    rsent = random.randrange(0, len(sentinels))
    rcont = random.randrange(0, len(controllers))
    rduel = random.randrange(0, len(duelist))
    rinit = random.randrange(0, len(initiators))
    rcomp = random.randrange(1, 5)
    finalcomp = ''
    finalcomp2 = ''
    if rcomp == 1:  # 1 Sentinels - 1 Controller - 2 Duelist - 1 Initiators

        compsent = sentinels[rsent]
        compcont = controllers[rcont]
        compduel = duelist[rduel]
        rduel = random.randrange(0, len(duelist))
        duelist.remove(duelist[rduel])
        compduel2 = duelist[rduel]
        compinit = initiators[rinit]
        finalcomp = '1 Sentinels - 1 Controller - 2 Duelist - 1 Initiators'
        finalcomp2 ='' + compsent + ' -' + compcont + ' -' + compduel + ' -' + compduel2 + ' - ' + compinit + '.'
    elif rcomp == 2:  # 2 Sentinels - 1 Controller - 1 Duelist - 1 Initiators

        compsent = sentinels[rsent]
        sentinels.remove(sentinels[rsent])
        rsent = random.randrange(0, len(sentinels))
        compsent2 = sentinels[rsent]
        compcont = controllers[rcont]
        compduel = duelist[rduel]
        compinit = initiators[rinit]
        finalcomp = '2 Sentinels - 1 Controller - 1 Duelist - 1 Initiators\n'
        finalcomp2 = '' + compsent + ' -' + compsent2 + ' -' + compcont + ' -' + compduel + ' - ' + compinit + '.'
    elif rcomp == 3:  # 0 Sentinels - 2 Controller - 1 Duelist - 2 Initiators

        compcont = controllers[rcont]
        controllers.remove(controllers[rcont])
        rcont = random.randrange(0, len(controllers))
        compcont2 = controllers[rcont]
        compduel = duelist[rduel]
        compinit = initiators[rinit]
        initiators.remove(initiators[rinit])
        rinit = random.randrange(0, len(initiators))
        compinit2 = initiators[rinit]

        finalcomp = '0 Sentinels - 2 Controller - 1 Duelist - 2 Initiators'
        finalcomp2 = '' + compcont + ' -' + compcont2 + ' -' + compduel + ' -' + compinit + ' - ' + compinit2 + '.'
    elif rcomp == 4:  # 1 Sentinels - 0 Controller - 2 Duelist - 2 Initiators
        compsent = sentinels[rsent]
        compduel = duelist[rduel]
        duelist.remove(duelist[rduel])
        rduel = random.randrange(0, len(duelist))
        compduel2 = duelist[rduel]
        compinit = initiators[rinit]
        initiators.remove(initiators[rinit])
        rinit = random.randrange(0, len(initiators))
        compinit2 = initiators[rinit]

        finalcomp = '1 Sentinels - 0 Controller - 2 Duelist - 2 Initiators'
        finalcomp2 = '' + compsent + ' -' + compduel + ' -' + compduel2 + ' -' + compinit + ' - ' + compinit2 + '.'
    embedcomp = {'comp': finalcomp, 'agents': finalcomp2, 'splash': splash}
    return embedcomp

