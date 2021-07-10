# FUNCTION IMPORTS
import time
from datetime import datetime

# DISCORD IMPORTS
import discord
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions

# API/Token IMPORTS
import Apis
import Token
import VALapi

global dumbmessage
dumbmessage = None

client = commands.Bot(command_prefix="!", help_command=None)


# @client.command()
# async def nasa(ctx):
#     await ctx.send(NASAapi.nasapic())

# Cat api function import

@client.command()  # Simple Help command
async def help(ctx):
    await ctx.send(
        '**!keengs - !cat - !dog - !meme - !booba - !agent - !comp "map" (please specify map :D) - !joke - !rude.**')
    return


@client.event  # Simple command to reply with poop when poop is said
async def on_message(message):
    await client.process_commands(message)
    # don't respond to ourselves
    if message.author == client.user:
        return

    if 'poop' in message.content.lower():
        await message.channel.send('Poopy pants :poop:')

    elif 'gay' in message.content.lower():
        await message.channel.send('you are gae')

    role = discord.utils.get(message.guild.roles, name="Cora")
    role2 = discord.utils.get(message.guild.roles, name="rassan")

    if role in message.author.roles:
        await message.channel.send(Apis.insult())
    elif role2 in message.author.roles:
        await message.channel.send('Rassan: ' + Apis.insult())
    return

    return


# Cat api function import
@client.command()
async def cat(ctx):
    await ctx.send(Apis.catapi())
    return


# Dog api function import
@client.command()
async def dog(ctx):
    await ctx.send(Apis.dogpic())
    return


# Joke Api function import
@client.command()
async def joke(ctx):
    await ctx.send(Apis.joke())
    return


# Meme api function import
@client.command()
async def meme(ctx):
    memedict = Apis.subbreddit()
    embed = discord.Embed(title=memedict['title'])
    embed.set_image(url=memedict['url'])
    await ctx.send(embed=embed)
    return


def guilds():
    guilds = client.guilds
    return guilds


def findmessage():
    return None


@client.command()
async def rude(ctx):
    print(ctx)
    await ctx.send(Apis.insult())
    return


@client.command()  # Boris Wanted Porn
@bot_has_permissions(manage_messages=True)
async def booba(ctx):
    await ctx.send(Apis.booba())
    time.sleep(3)
    await ctx.channel.purge(limit=2)
    return


@client.command()  # Clear command
@bot_has_permissions(manage_messages=True)
@has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    if 0 < amount < 100:
        await ctx.channel.purge(limit=amount)
        await ctx.send('Messages have been deleted' + str(amount + 1))
    else:
        await ctx.send('Your number is too large <3')
    return


@client.event  # Reaction command lines
async def on_raw_reaction_add(ctx):
    # dd/mm/YY H:M:S
    msgreact = ctx.message_id  # Adding message ID to a var
    # reaction = ctx.
    global msgid
    if msgreact == msgid:
        channel = await client.fetch_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)
        reaction = discord.utils.get(message.reactions, emoji=ctx.emoji.name)
        inter_total = ["✅", "❌"]

        if ctx.emoji.name not in inter_total:
            await reaction.remove(ctx.member)

        await client.change_presence(status=discord.Status.online, activity=discord.Game('Running Server '
                                                                                         'Refresh'))
        x = hackkeengs()
        time.sleep(2)  # Sleeping for 1 seconds
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))
        await message.edit(content=x)
        return


# noinspection DuplicatedCode
def hackkeengs():  # MY bread and butter function
    r = requests.get('https://mtxserv.com/api/v1/viewers/game?type=minecraft&ip=game-fr-14.mtxserv.com&port=27180')

    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    lastupdate = "**Last Update**  = " + ' ' + dt_string + ''

    json_data = r.json()
    is_online = json_data['is_online']
    # ip = json_data ['ip']
    # host_name = json_data ['params']['host_name']
    # joinlink = json_data ['params']['joinlink']
    max_slots = json_data['params']['max_slots']
    players = json_data['params']['players']
    # print(json_data)

    # if server is online or offine - serveronoff

    if is_online:
        serveronoff = '**Server Online**'
    else:
        serveronoff = '**SERVER IS FUCKING DEAD @LEAROY ASAP SAVE IT NOW**'
    # Player number

    playernumber = len(players)
    # Sending message or not

    names = '**Connected Players: **'
    if playernumber > 0:
        for player in players:
            names += player['player'] + ' **-** '
        names = names[:-7]
    else:
        names = '**No one is on , sadge....GET ON YOU DUMBASS**'
    # Actual code

    x = ('...HACKING SERVER...\n'
         '' + serveronoff + '\n'
                            '**Server-IP: ** 51.254.57.60:27180\n'
                            '**Online Player**: ' + str(playernumber) + '/' + str(max_slots) + '\n'
                                                                                               '' + names + '\n'
                                                                                                            '' + lastupdate + ' **UTC +3**')
    return x


@client.command()  # If refresh function for keengs does not work (manual)
async def keengs(ctx):
    x = hackkeengs()
    await ctx.send(x)
    return


@client.command()  # A command to show all map availbale
async def map(ctx):
    await ctx.send('Haven - Split - Bind - IceBox - Breeze - Acesnt ')


@client.command()
async def comp(ctx, choice='breeze'):
    if map == 'breeze':
        choice = 'https://media.valorant-api.com/maps/2fb9a4fd-47b8-4e7d-a969-74b4046ebd53/splash.png'
    elif map == 'split':
        choice = 'https://media.valorant-api.com/maps/d960549e-485c-e861-8d71-aa9d1aed12a2/splash.png'
    elif map == 'bind':
        choice = 'https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/splash.png'
    elif map == 'haven':
        choice = 'https://media.valorant-api.com/maps/2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/splash.png'
    elif map == 'icebox':
        choice = 'https://media.valorant-api.com/maps/e2ad5c54-4114-a870-9641-8ea21279579a/splash.png'
    elif map == 'ascent':
        choice = 'https://media.valorant-api.com/maps/7eaecc1b-4337-bbf6-6ab9-04b8f06b3319/splash.png'
    else:
        embedcomp = VALapi.valcomp()
        choice = embedcomp['splash']
    embedcomp = VALapi.valcomp()
    embed = discord.Embed(title='Here are your agents and composition!', description='')
    embed.add_field(name='Agents', value=embedcomp['agents'])
    embed.add_field(name='Composition', value=embedcomp['comp'], inline=False)
    embed.set_image(url=choice)
    await ctx.send(embed=embed)


@client.command()
async def agent(ctx):
    valdict = VALapi.valagent()
    embed = discord.Embed(title='Here is your agent!', description='' + valdict['name'] + '')
    embed.set_image(url=valdict['pic'])
    embed.add_field(name='Role', value=valdict['role'], inline=False)
    embed.add_field(name='Description', value=valdict['desc'])
    await ctx.send(embed=embed)
    return


# @client.command()
# async def Message(ctx) :
#     await ctx.send('Dummy message')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))
    # print(guilds()[0].id)                                                                           #Server ID
    channel = discord.utils.get(client.get_all_channels(), guild__name='Keengs', name='server-info')  # Channel name
    # print(channel)
    global msgid
    msgid = 855148407302651924
    # global dumbmessage
    # dumbmessage = await channel.fetch_message(msgid)
    # print (dumbmessage.content)
    global msglist
    msglist = channel.history(limit=1)
    msglist = await msglist.flatten()
    # print(msglist)
    client.get_channel(852117601803042868)
    # print(Channelname)
    # await dumbmessage.add_reaction('🔄')
    return


client.run(Token.TOKEN)

# PARMS OBJECT LIST
# {'is_online': True,
#  'ip': 'game-fr-14.mtxserv.com',
#  'port': '27180',
#  'game': 'minecraft',
#  'params': {'gametype': 'SMP',
#  'host_name': 'Keengs Do 1.17 !',
#  'joinlink': 'minecraft://game-fr-14.mtxserv.com:27185/',
#  'map': 'world',
#  'max_slots': '40',
#  'password': False,
#  'players': [],
#  'plugins': 'CraftBukkit on Bukkit 1.17-R0.1-SNAPSHOT: DeathCounter 1.1;
#   LuckPerms 5.3.47; SinglePlayerSleep 1.13_2.13.46;
#    TreeFeller 1.16.1', 'teams': [], 'type': 'minecraft', 'used_slots': '0', 'version': '1.17'}}
