import aiohttp
from bs4 import BeautifulSoup
import randomheaders
from discord.ext import commands
import random

# Bot token from discord dev website
BOT_TOKEN = "PASTE YOUR DISCORD BOT TOKEN HERE"

# bot object and set command prefix to "`"
bot = commands.Bot(command_prefix='`')


# when bot is running print the bot tokens name
@bot.event
async def on_ready():
    print("Using Bot Token for:", bot.user.name)


# async function for aiohttp to fetch given url and download html
async def fetch_async(url):
    # create aiohttp session
    async with aiohttp.ClientSession() as session:
        # get page for given url with random header to prevent bot flag
        async with session.get(url, headers=randomheaders.LoadHeader()) as resp:
            # download html and send back to function that called
            return await resp.text()


@bot.command()
async def word(ctx, message):
    words_arr = []
    # get only first letter sequence in message
    first_word = message.split(' ')[0]
    # base url for merriam.com scrabble finder
    scrabble_base_url = "https://scrabble.merriam.com/words/with/"
    # url to get and find words (passed into fetch_async function)
    url_with_word = scrabble_base_url + first_word
    # get html content of url with aiohttp
    content = await fetch_async(url_with_word)
    # pass html content into beautiful soup to parse
    soup = BeautifulSoup(content, 'lxml')

    # loop through all div tags with the class "sbl_word_group open" (this contains all the words)
    for groups in soup.find_all('div', class_='sbl_word_group open'):
        # get unordered list html which contains all the words
        group_ul = groups.find('ul', class_='wres_ul')
        # loop through all words in list items
        for group_li in group_ul.find_all('li'):
            # save each words and replace new lines with blanks
            words_containing = group_li.text.replace('\n', '')
            # add word to array
            words_arr.append(words_containing)

    # send random word from words array
    await ctx.send(random.choice(words_arr))

# run bot
bot.run(BOT_TOKEN)
