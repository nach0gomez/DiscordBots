import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv

def run_bot():
    # load variables from .env file
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    # able to read messages and read commands
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    voice_clients = {}
    yt_dl_options = { "format": "bestaudio/best" }
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    
    # video non (just capture audio from youtube video)
    ffmpeg = { "options": "-vn" }
    
    @client.event
    async def on_ready():
        print(f'¡{client.user} le está pegando al tin!')
        
    @client.event
    async def on_message(message):
        
        if message.content.startswith('-play'):
                try:
                    voice_client = await message.author.voice.channel.connect()
                    voice_clients[voice_client.guild.id] = voice_client
                except Exception as e:
                    await print(f'¡Error! {e}')         
        
                try:
                    url = message.content.split()[0]
                    
                    loop = asyncio.get_event_loop()
                    
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                    song = data['url']
                    # This launches a sub-process to a specific input file given.
                    player = discord.FFmpegPCMAudio(song, **ffmpeg)
                    
                    voice_clients[message.guild.id].play(player) 
                    
                except Exception as e:
                    await print(f'¡Error! {e}')
        
    client.run(TOKEN)    
    
        # ! test this code
        # if message.author == client.user:
        #     return
        
        # if message.content.startswith('-play'):
        #     channel = message.author.voice.channel
        #     if channel:
        #         try:
        #             voice_clients[message.guild] = await channel.connect()
        #             voice_clients[message.guild].play(discord.FFmpegPCMAudio(ytdl.extract_info(message.content[6:], download=False)['url'], **ffmpeg))
        #         except Exception as e:
        #             await print(f'¡Error! {e}')           
        #     else:
        #         await message.channel.send('¡No estás en un canal de voz!')
        
        # if message.content.startswith('-leave'):
        #     if message.guild in voice_clients:
        #         await voice_clients[message.guild].disconnect()
        #         del voice_clients[message.guild]
        #     else:
        #         await message.channel.send('¡No estoy en un canal de voz!')
    
    