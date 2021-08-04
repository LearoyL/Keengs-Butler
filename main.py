# FUNCTION IMPORTS
import os
import random
import time
from datetime import datetime

# DISCORD IMPORTS
import discord
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions

# API/Token IMPORTS
import Apis
import VALapi
from keep_alive import keep_alive

global dumbmessage
dumbmessage = None

client = commands.Bot(command_prefix="!", description="A bot to handle all your Keeng needs", help_command=None)

# TODO: figure out how to change an array then change it to a string after.

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@client.command()
async def tictac(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        embed = discord.Embed(title='TicTacToe')
        embed.add_field(name='\u200b', value=':white_large_square: :white_large_square: :white_large_square:')
        embed.add_field(name='\u200b', value=':white_large_square: :white_large_square: :white_large_square:',
                        inline=False)
        embed.add_field(name='\u200b', value=':white_large_square: :white_large_square: :white_large_square:',
                        inline=False)

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is being played idoit, wait your turn before starting another.")


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!, nice one!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Its a tie... You both lost.")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("Wait your turn motherfucker.")
    else:
        await ctx.send("What are you trying to place? do !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@ttt.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Its a 2 player game , get some friends.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Pick a number dofus, 1 through 9 smart one.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Its a number after fuckface, wakeup.")


@client.command()
async def mkpoll(ctx, question='', *options):
    numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣")
    author = ctx.message.author.name
    errorsyn = 'Use this format dummy.\n' \
               '"!mkpoll "title" option1 option2 etc "'

    if len(options) > 5:
        embed = discord.Embed(title='Poll-Error',
                              description='You can only do 5 options dumbass.',
                              colour=ctx.author.color,
                              timestamp=datetime.utcnow())
        embed.set_footer(text='Poll by ' + ctx.message.author.name, icon_url="https://i.imgur.com/LnsoG2F.png")
        await ctx.send(embed=embed)

    elif question == '':
        embed = discord.Embed(title='Poll-Error',
                              description=errorsyn,
                              colour=ctx.author.color,
                              timestamp=datetime.utcnow())
        embed.set_footer(text='Poll by ' + ctx.message.author.name, icon_url="https://i.imgur.com/LnsoG2F.png")
        await ctx.send(embed=embed)
    elif options == ():
        embed = discord.Embed(title='Poll-Error',
                              description=errorsyn,
                              colour=ctx.author.color,
                              timestamp=datetime.utcnow())
        embed.set_footer(text='Poll by ' + ctx.message.author.name, icon_url="https://i.imgur.com/LnsoG2F.png")
        await ctx.send(embed=embed)
    elif question != '' and options != '':
        embed = discord.Embed(title='Poll',
                              description=question,
                              colour=ctx.author.color,
                              timestamp=datetime.utcnow())
        fields = [('Options', '\n'.join([f'{numbers[idx]} {option}' for idx, option in enumerate(options)]), False),
                  ('Instructions', 'Just react, it is really not that hard!', False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(text='Poll by ' + ctx.message.author.name, icon_url="https://i.imgur.com/LnsoG2F.png")
        message = await ctx.send(embed=embed)

        for emoji in numbers[:len(options)]:
            await message.add_reaction(emoji)
    if ctx.channel.guild.me.guild_permissions.manage_messages:
        await ctx.message.delete()
    return


# Cat api function import
@client.command()  # Simple Help command
async def help(ctx):
    print(ctx.author)
    valhelp = '!agent - !comp "map" (please specify map :D)'
    apihelp = '!cat - !dog - !meme - !booba'
    commonhelp = '!flipcoin - !joke - !rude - !mkpoll'
    embed = discord.Embed(title='Help Command',
                          description='Here, ' + str(ctx.author.mention) + ', these are the available commands.',
                          colour=ctx.author.color,
                          timestamp=datetime.utcnow())
    embed.add_field(name='Valorant Commands', value=valhelp, inline=False)
    embed.add_field(name='Api Commands', value=apihelp, inline=False)
    embed.add_field(name='Extra Commands', value=commonhelp, inline=False)

    embed.set_footer(text='\u200b', icon_url="https://i.imgur.com/LnsoG2F.png")
    await ctx.send(embed=embed)
    return


@client.command()
async def everyones(ctx):
    await ctx.send(ctx.message.guild.default_role)
    return


@client.command()
async def flip(ctx):
    coin = Apis.coin()
    if coin == 'Heads':
        choice = 'https://cdn.discordapp.com/attachments/807717801128624168/868163587615645706/Hotpot1.png'
    else:
        choice = 'https://cdn.discordapp.com/attachments/807717801128624168/868162855034310656/Hotpot.png'
    embed = discord.Embed(title='A coin was flipped!', description='')
    embed.set_image(url=choice)
    await ctx.send(embed=embed)
    return


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')
    time.sleep(3)
    await ctx.channel.purge(limit=2)
    return


@client.event  # Simple command to reply with poop when poop is said
async def on_message(message):
    await client.process_commands(message)
    # don't respond to ourselves
    name = message.author.name
    if message.author == client.user:
        return

    if 'poop' in message.content.lower():
        await message.channel.send('Poopy pants :poop:')

    elif 'gay' in message.content.lower():
        await message.channel.send('you are gae')

    role = discord.utils.get(message.guild.roles, name="Cora-installed")
    role2 = discord.utils.get(message.guild.roles, name="rassan")
    role3 = discord.utils.get(message.guild.roles, name="Compliment")
    if role in message.author.roles:
        await message.channel.send(name + ' - ' + Apis.insult())
    elif role2 in message.author.roles:
        await message.channel.send(name + ' - ' + Apis.insult())
    elif role3 in message.author.roles:
        await message.channel.send(name + ' - ' + Apis.Compliment())
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
async def comp(ctx, map='breeze'):
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


TOKEN = os.environ['TOKEN']
keep_alive()
client.run(TOKEN)
