import discord
from discord.ext import commands
import requests
import re
import asyncio

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# API endpoint
api_url = 'https://api.api-aries.online/v1/checkers/safe-url/?url='
# Your token and token type
token_type = 'token type' #learn more on their docs: https://support.api-aries.online/hc/articles/1/3/4/safe-url-api
api_key = 'API token' #learn more on their docs: https://support.api-aries.online/hc/articles/1/3/4/safe-url-api


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    
    url_pattern = re.compile(r'https?://\S+')

    
    urls = url_pattern.findall(message.content)

    for url in urls:
        
        safe, safe_message = check_link_safety(url)
        if not safe:
            embed = discord.Embed(
                title="Unsafe URL Warning",
                description=f"The URL `{url}` is not safe. \n\n Reason:\n {safe_message}",
                color=discord.Color.red()
            )
            embed.set_footer(text="Made by API-Aries", icon_url="https://support.api-aries.online/favicon/icon-144x144.png")
            warning_message = await message.channel.send(embed=embed)
            await message.delete()

            
            await asyncio.sleep(90)
            await warning_message.delete()


def check_link_safety(url):
    try:
        
        headers = {
            'Type': token_type,
            'APITOKEN': api_key
        }

        
        response = requests.get(api_url + url, headers=headers)

        
        if response.status_code == 200:
            data = response.json()
            safe = data['safe']
            message = data['message']
            return safe, message
        else:
            return False, f"Failed to check safety: {response.status_code}"
    except Exception as e:
        return False, f"An error occurred: {e}"


# bot token
bot.run('MTIwODU0MTM5ODk3NTExOTQwMA.G2tCa0.gwwE6HT9-EPmVWKX-uUyUExA-u-D9DfkDImwSQ')
