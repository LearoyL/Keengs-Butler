# FUNCTION IMPORTS
import os
import random
import time
import boobaapi
from datetime import datetime

# DISCORD IMPORTS
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions

# API/Token IMPORTS
import Apis
import VALapi
from keep_alive import keep_alive

keep_alive()

TOKEN = os.environ['TOKEN']
client = commands.Bot(command_prefix="!", description="A bot to handle all your Keeng needs", help_command=None)

player1 = ''
player2 = ''
turn = ''
gameOver = True

hangmanOver = True
hangmanemptyspace = []
hangmancount = 0
letterbase = ''

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
    global finalboard
    global gamemessage
    global board

    if gameOver:
        await client.change_presence(status=discord.Status.online, activity=discord.Game("Hold on X'O is going on!"))
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:", ]
        turn = ""
        gameOver = False
        count = 0
        # fakeboard = ''
        # for i, x in enumerate(board):
        #     fakeboard += x
        #     if i == 2 or i == 5 or i == 8:
        #         fakeboard += '\n'
        # finalboard = fakeboard
        player1 = p1
        player2 = p2
        embed = discord.Embed(title='TicTacToe', )
        embed.add_field(name='\u200b', value=fixboard(board))
        gamemessage = await ctx.send(embed=embed)

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
    global finalboard
    global gamemessage

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
                if turn == player1:
                    embed = discord.Embed(title='TicTacToe', description="It is <@" + str(player2.id) + ">'s turn.")
                    embed.add_field(name='\u200b', value=fixboard(board))

                elif turn == player2:
                    embed = discord.Embed(title='TicTacToe', description="It is <@" + str(player1.id) + ">'s turn.")
                    embed.add_field(name='\u200b', value=fixboard(board))
                await gamemessage.edit(embed=embed)

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver:
                    await ctx.send(mark + " wins!, nice one!")
                    await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Its a tie... You both lost.")
                    await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))

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
        await ctx.send("What are you trying to place? do !tictac command.")
    await ctx.message.delete()


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@client.command()
async def tictacend(ctx):
    global gameOver
    if gameOver:
        await ctx.send('There are no ongoing TicTacToe games.')
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))
    elif not gameOver:
        gameOver = True
        await ctx.send('TicTacToe game has ended. You can start one now.')
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))


@tictac.error
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
    # author = ctx.message.author.name
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
    valhelp = '!agent - !comp "map" (please specify map :D)'
    apihelp = '!cat - !dog - !meme - !booba'
    commonhelp = '!flip - !joke - !rude - !mkpoll -!quote(!addq)'
    gamehelp = '!tictac (@ 2 people to play) - !hangman - !roll - !numbergen'
    embed = discord.Embed(title='Help Command',
                          description='Here, ' + str(ctx.author.mention) + ', these are the available commands.',
                          colour=ctx.author.color,
                          timestamp=datetime.utcnow())
    embed.add_field(name='Valorant Commands', value=valhelp, inline=False)
    embed.add_field(name='Api Commands', value=apihelp, inline=False)
    embed.add_field(name='Extra Commands', value=commonhelp, inline=False)
    embed.add_field(name="Game'ish Commands", value=gamehelp, inline=False)

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

    elif ('poop' in message.content.lower()) and ('gay' in message.content.lower()) and ('no u' in message.content.lower()) and ('fuck you' in message.content.lower()):
        x = 'Poopy pants :poop:' + '\n' + 'you are gae'
    elif 'poop' in message.content.lower():
        x = 'Poopy pants :poop:'
    elif 'gay' in message.content.lower():
        x = 'you are gae'
    elif 'no u' in message.content.lower():
        x = 'No u!'
    elif 'fuck you' in message.content.lower():
        x = 'No FUCK you!'
    await message.channel.send(x)

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


# Appeding qoute to DB
def addquote(quote):
    now = datetime.now()
    d4 = now.strftime("%b-%Y")
    fileq = open('quoteDB.txt', 'a')
    fileq.write(quote + ' - ' + d4 + '\n')
    fileq.close()
    return


# Grabbing a line
def getquote():
    fileq = open('quoteDB.txt', 'r')
    list_quote = []
    for line in fileq:
        stripline = line.strip()
        list_quote.append(stripline)
    random_quote = random.randrange(0, len(list_quote))
    global final_quote
    final_quote = list_quote[random_quote]
    return final_quote


# Grab a specific Line of quote
def get_specific_quote(specific_global):
    global specific_quote
    fileq = open('quoteDB.txt', 'r')
    list_quote = []
    for line in fileq:
        stripline = line.strip()
        list_quote.append(stripline)
    lowered_list_quote = [x.lower() for x in list_quote]
    specific_quote = [i for i in lowered_list_quote if specific_global.lower() in i]
    print(specific_quote)
    return specific_quote


def checking_specific():
    global specific
    global final_specific_quote
    final_specific_quote = ''
    # lowered_list = [x.lower for x in specific_quote]
    if len(specific_quote) == 0:
        final_specific_quote = 'There are no quotes with that person' + specific_global + '. Give them one.'
    elif len(specific_quote) != 0:
        final_specific_quote_number = random.randrange(0, len(specific_quote))
        print(specific_quote)
        final_specific_quote = specific_quote[final_specific_quote_number]
        pass


@client.command()
async def addq(ctx, quote=''):
    if quote != '':
        addquote(quote)
        await ctx.send('Quote has been added')
    elif quote == '':
        await ctx.send('Add quote mf, "*Insert quote here* - *Author* - *Date(m/y)*"')
    return


@client.command()
async def quote(ctx, specific=''):
    global specific_quote
    global specific_global
    specific_global = specific
    getquote()
    global final_quote
    if specific == '':
        await ctx.send(final_quote)
    elif specific != '':
        get_specific_quote(specific_global)
        print(specific)
        checking_specific()
        print(final_specific_quote)
        await ctx.send(final_specific_quote)

    return


def fixboard(board):
    fakeboard = ''
    for i, x in enumerate(board):
        fakeboard += x
        if i == 2 or i == 5 or i == 8:
            fakeboard += '\n'
    finalboard = fakeboard
    return finalboard


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
    await ctx.send(boobaapi.boooba(), delete_after=10)
    await ctx.message.delete()
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


@clear.error
async def clear_error(ctx, error):
    message = ''
    if isinstance(error, commands.MissingPermissions):
        message = 'You are a low idoit, cant do this.'
    await ctx.send(message)


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
        serverlist = Apis.hackkeengs()
        embed = discord.Embed(title='**UKH** Minecraft Server!', description='',
                              colour=0x9b59b6,
                              timestamp=datetime.utcnow())
        embed.add_field(name='Server Status:', value=serverlist[0], inline=False)
        embed.add_field(name='Sever IP:', value='51.255.235.102:27280', inline=False)
        embed.add_field(name='Players:', value='' + str(serverlist[1]) + '/' + str(serverlist[2]) + '', inline=False)
        embed.add_field(name='Online Players:', value=serverlist[3], inline=False)

        time.sleep(2)  # Sleeping for 1 seconds
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))
        await message.edit(embed=embed)
        return


#
# @client.command()  # If refresh function for keengs does not work (manual)
# async def keengs(ctx):
#     x = Apis.hackkeengs()
#     await ctx.send(x)
#     return


@client.command()
async def valmap(ctx):
    await ctx.send('Haven - Split - Bind - IceBox - Breeze - Acesnt ')


@client.command()
async def comp(ctx, valmap='breeze'):
    if valmap == 'breeze':
        choice = 'https://media.valorant-api.com/maps/2fb9a4fd-47b8-4e7d-a969-74b4046ebd53/splash.png'
    elif valmap == 'split':
        choice = 'https://media.valorant-api.com/maps/d960549e-485c-e861-8d71-aa9d1aed12a2/splash.png'
    elif valmap == 'bind':
        choice = 'https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/splash.png'
    elif valmap == 'haven':
        choice = 'https://media.valorant-api.com/maps/2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/splash.png'
    elif valmap == 'icebox':
        choice = 'https://media.valorant-api.com/maps/e2ad5c54-4114-a870-9641-8ea21279579a/splash.png'
    elif valmap == 'ascent':
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
    return


@client.command()
async def agent(ctx):
    valdict = VALapi.valagent()
    embed = discord.Embed(title='Here is your agent!', description='' + valdict['name'] + '')
    embed.set_image(url=valdict['pic'])
    embed.add_field(name='Role', value=valdict['role'], inline=False)
    embed.add_field(name='Description', value=valdict['desc'])
    await ctx.send(embed=embed)
    return


@client.command()
async def numbergen(ctx, n1: int, n2: int):
    if n1 == '' or n2 == '':
        await ctx.send('Use the format "!numbergen number(1) number(2)"')
    elif n1 > n2:
        await ctx.send('Make sure the first number is smaller than the second.')
    elif n1 < 0 or n2 < 0:
        await ctx.send('Use +ive numbers... smh.')
    else:
        number = random.randrange(n1, n2)
        await ctx.send('You randomly generated number is ' + str(number))
    return


@numbergen.error
async def numbergen_error(ctx, error):
    message = ''
    if isinstance(error, commands.MissingRequiredArgument):
        message = 'Use the format "!numbergen number(1) number(2)"'
    await ctx.send(message)


@client.command()
async def roll(ctx, die_string: str):
    dice, value = (int(term) for term in die_string.split("d"))

    if dice <= 25:
        rolls = [random.randint(1, value) for i in range(dice)]

        await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

    else:
        await ctx.send("I can't roll that many dice. Please try a lower number of dice.")


@roll.error
async def roll_error(ctx, error):
    message = ''
    if isinstance(error, commands.MissingRequiredArgument):
        message = 'Use the format "!roll (number of dice)d(number of sides)"'
    await ctx.send(message)


@client.command()
async def hangman(ctx):
    global hangword
    global spaces
    global spacesword
    global hangingman
    global hangmanOver
    global listhangword

    if hangmanOver:
        hangmanOver = False
        hangword = Apis.randomword()
        spaces = len(hangword)
        spacesword = ':blue_square: ' * int(spaces)
        fixhangword(hangmanemptyspace, spaces)
        await client.change_presence(status=discord.Status.online,
                                     activity=discord.Game("Hold on Hangman is going on!"))
        embed = discord.Embed(title='HangMan with Keengs :skull:',
                              description='Guess by **!hang "letter"**',
                              colour=ctx.author.color,
                              timestamp=datetime.utcnow())
        embed.add_field(name='Your word has ' + str(spaces) + ' letters.', value=spacesword)
        hangingman = await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='HangMan with Keengs :skull:',
                              description='An ongoing game is going on.',
                              colour=ctx.author.color,
                              timestamp=datetime.utcnow())
        await ctx.send(embed=embed, delete_after=5.0)
    print(hangword)
    listhangword = list(hangword)
    # print(listhangword)
    # print(space)
    # print(spacesword)

    return


@client.command()
async def hang(ctx, letter=''):
    global hangword
    global spaces
    global spacesword
    global hangingman
    global hanger_author
    global hangmanemptyspace
    global hangmanstring
    global listhangword
    global hangmancount
    global letterbase
    global hangmanmessage
    global hangmanOver
    # print(ctx.message)
    # hanger_author = hanger
    # name = ctx.message.author.name
    # id = ctx.message.author.discriminator
    #  = name+'#'+id
    if not hangmanOver:
        if letter == '':
            await ctx.send('Please add a letter dumbdumb.')
            await ctx.message.delete()
        elif letter in letterbase:
            await ctx.send('You already have guessed this letter, try another!', delete_after=5.0)
            await ctx.message.delete()
        elif letter in hangword:
            letterbase += letter
            changehang = [i for i in range(len(listhangword)) if listhangword[i] == letter]
            print(changehang)
            for x in changehang:
                hangmanemptyspace[x] = Apis.letterdict[letter]

            printhangman(hangmanemptyspace)
            embed = discord.Embed(title='HangMan with Keengs :skull:',
                                  description='Correct guess ' + format(ctx.message.author.mention) + ', next letter.',
                                  colour=ctx.author.color,
                                  timestamp=datetime.utcnow())
            embed.add_field(name='Your word has ' + str(spaces) + ' letters.', value=hangmanstring)
            embed.add_field(name='Remaining Lives', value='' + str(hangmancount) + '/' + str(spaces), inline=False)
            embed.set_footer(text='*!hang "letter"*')
            hangmanchecker(hangmanstring)
            await ctx.message.delete()
            await hangingman.edit(embed=embed)

        elif str(letter) not in hangword:
            letterbase += letter
            hangmancount += 1
            printhangman(hangmanemptyspace)

            embed = discord.Embed(title='HangMan with Keengs :skull:',
                                  description='Wrong guess ' + format(ctx.message.author.mention) + ', try again.',
                                  colour=ctx.author.color,
                                  timestamp=datetime.utcnow())
            embed.add_field(name='Your word has ' + str(spaces) + ' letters.', value=hangmanstring)
            embed.add_field(name='Remaining Lives', value='' + str(hangmancount) + '/' + str(spaces), inline=False)
            embed.set_footer(text='*!hang "lettter"*')
            wrong_letter = Apis.letterdict[letter]
            await hangingman.add_reaction(wrong_letter)
            await hangingman.edit(embed=embed)
            await ctx.message.delete()
            # hangmanlifechecker(spaces,hangmancount)
            assert hangmanlifechecker(spaces, hangmancount)[1] == hangmanOver
            embed = discord.Embed(title='HangMan with Keengs :skull:',
                                  description='Wrong guess ' + format(ctx.message.author.mention) + ', try again.',
                                  colour=ctx.author.color,
                                  timestamp=datetime.utcnow())
            embed.add_field(name='Your word has ' + str(spaces) + ' letters.', value=hangmanstring)
            embed.add_field(name=hangmessage, value='' + str(hangmancount) + '/' + str(spaces), inline=False)
            embed.set_footer(text='*!hang "lettter"*')
            await hangingman.edit(embed=embed)
            hangmanchecker(hangmanstring)
    if hangmanOver:
        await ctx.send('Start a game to play mf.', delete_after=5.0)


@client.command()
async def hangmanend(ctx):
    global hangmanOver
    if hangmanOver:
        await ctx.send('There are no on going HangMan games', delet_after=5.0)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))
    else:
        hangmanOver = True
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))


def fixhangword(hangmanemptyspace, spaces) -> list:
    emptyemoji = ':blue_square:'
    i = 0
    while i < int(spaces):
        hangmanemptyspace.append(emptyemoji)
        i += 1
    # print(hangmanemptyspace)
    return hangmanemptyspace


def printhangman(hangmanemptyspace):
    global hangmanstring
    hangmanstring1 = ''
    for i, x in enumerate(hangmanemptyspace):
        hangmanstring1 += x + ' '
    hangmanstring = hangmanstring1
    # print(hangmanstring1)
    return hangmanstring


def hangmanchecker(hangmanstring):
    global hangmanOver
    if ':blue_square:' in hangmanstring:
        hangmanOver = False
    else:
        hangmanOver = True
    return hangmanOver


def hangmanlifechecker(hangmancount, spaces):
    global hangmanOver
    global hangmessage
    hangmessage = ''
    if hangmancount > int(spaces):
        hangmanOver = False
        hangmessage = 'Remaining lives'
    if hangmancount == int(spaces):
        hangmanOver = False
        hangmessage = 'This is your last life!'
    if hangmancount < int(spaces):
        hangmanOver = True
        hangmessage = 'You have lost!.'
    return hangmessage, hangmanOver


@client.event
async def on_voice_state_update(member, before, after):
    channel = before.channel or after.channel
    role_id = 893870297017630741

    room_id = 893863983004663870
    room_text = client.get_channel(893864066613923841)
    if channel.id == room_id:
        if before.channel is None and after.channel is not None:
            await room_text.send('<@' + str(member.id) + '> Is in the house <@&893870297017630741>')
            # member joined a voice channel,
        elif before.channel is not None and after.channel is None:
            pass
            # member left a voice channel
    return


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('I AM THE BEST BOT'))
    # print(guilds()[0].id)                                                                           #Server ID
    channel = discord.utils.get(client.get_all_channels(), guild__name='UKH SoM UG2',
                                name='server-info')  # Channel name
    # print(channel)
    global msgid
    msgid = 904414305024352266
    # global dumbmessage
    dumbmessage = await channel.fetch_message(msgid)
    # print (dumbmessage.content)
    global msglist
    msglist = channel.history(limit=1)
    msglist = await msglist.flatten()
    # print(msglist)
    client.get_channel(852117601803042868)
    # print(Channelname)
    # await dumbmessage.add_reaction('🔄')
    return


##
# @client.command()
# async def Message(ctx) :
#     await ctx.send('Dummy message')
my_secret = os.environ['TOKEN']
client.run(my_secret)