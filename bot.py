import os
import json
import re
import configparser
import discord
import datetime
import random
import asyncio
#import asyncpg
import requests
import pprint as pp
from random import randint as ri
from bs4 import BeautifulSoup as bs
from requests_html import AsyncHTMLSession as ahtmls
from discord.utils import get
from discord.ext import commands
from discord import Intents
from imgurpython import ImgurClient



config = configparser.ConfigParser()
config.read('config.ini')
intents_all = Intents.all()
client = commands.Bot(command_prefix="~", intents=intents_all)
ch_id = config['discord']['ch_id']
msg_id = config['discord']['msg_id']
#imgur
c_id = config['imgur']['c_id']
c_sec = config['imgur']['c_sec']
access_token = config['imgur']['access']
refresh_token = config['imgur']['refresh']
#imgur = ImgurClient(c_id, c_sec, access_token, refresh_token)
# TODO : refactor code into class structure
# global vars

mode = 1
#print(imgur.credits)
async def run():
   try:
       client.run(config['discord']['token'])
   except KeyboardInterrupt:
       await client.logout()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #ch = client.get_channel(ch_id)
    #await client.change_presence(activity=discord.Game(name='Exploring the 「Library」'))
    await client.change_presence(activity=discord.Game(name='with your soul'))
    

@client.command(name='s_g')
@commands.has_role('giveaway')
async def startg(ctx, mins:int, prize:str):
    embed = discord.Embed(title='Giveaway!', description=f'{prize}', color=ctx.author.color)
    end = datetime.datetime.utcnow() + datetime.timedelta(minutes = mins)
    embed.add_field(name='Ends at:', value=f'{end} UTC')
    embed.set_footer(text=f'Ends {mins} minutes from now!')
    my_msg = await ctx.send(embed=embed)
    await my_msg.add_reaction('💯')
    # create a task
    await asyncio.sleep(mins)
    # create a task
    new_msg = await ctx.channel.fetch_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)
    await ctx.send(f'Congratulations {winner.mention} won {prize}!')

@client.command(name='new')
async def new_classes(ctx, num:int=0):
    URL = 'https://sinoalice.game-db.tw/?_lang_=en'
    '''
    page = requests.get(URL)
    soup = bs(page.content, 'html.parser')
    pp.pprint(page.content)
    '''
    asession = ahtmls()
    r = await asession.get(URL)
    await r.html.arender()
    items = r.html.find(selector='div.itemBlock.char')
    for i, el in enumerate(items):
        if i < num:
            info = el.text.split('\n')
            img_ext = el.find(selector='img[src^=\'/images/character\']')[0].attrs['src']
            img_url = 'https://sinoalice.game-db.tw/'+img_ext
            embed = discord.Embed(title=str(info[0]), description='\n'.join(info[1:]))
            embed.set_thumbnail(url=img_url)
            await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command(name='job')
async def jobs(ctx, char:str, type:str):
    URL = 'https://sinoalice.game-db.tw/characters/?_lang_=en'
    print(URL)

@client.command(name='straw')
async def strawpoll(ctx):
    args = ctx.message.content.split('|')
    asession = ahtmls()
    if not ctx.message.author.bot:
        try:
            data = {'title':args[1], 'options': args[2:], 'multi':'true'}
            poll = await asession.post(
                'https://www.strawpoll.me/api/v2/polls',
                json=data,
                headers={
                    'Content-Type': 'application/json',
                    }
            )
            print(poll.json())    
            await ctx.send('https://strawpoll.me/' + str(poll.json()['id']))
            await ctx.message.delete()

        except KeyError:
            return 'Invalid arguments.'

@client.command(name='imgur')
async def upload_media(ctx):
    media = ctx.message.attachments
    if not media:
        emb = discord.Embed(title='No media files detected.', description='Please attach an image(.png/.jpeg) or .gif file before running the command!')
        await ctx.send(embed=emb)
        return
    print(media[0],'/n')
    url = "https://api.imgur.com/3/image"
    payload = {
        'image': media[0].url,
        'type': 'url',
                }
    files = [
    ]
    headers = {
    'Authorization': f'Client-ID {c_id}'
    }
    response = requests.request("POST", url, headers=headers, data = payload, files = files)
    if response.ok:
        print(response.json())
        print(response.text.encode('utf8'))
        img_url = response.json()['data']['link']
        emb = discord.Embed(title='Link available:', description=img_url)
        emb.set_thumbnail(url=img_url)
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title='Command Failed', description=response.json()['data']['error'])
        await ctx.send(embed=emb)
        
@client.command(name='bonus')
async def bonus(ctx, num:int=10, delay:int=2):
    for _ in range(num):
        await ctx.send(content='$m', delete_after=delay)
        await asyncio.sleep(delay)

@client.command(name='movie')
async def mov1(ctx):
    options = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣']
    times   = ['⏱️', '⏰', '🕰️'] 
    emb=discord.Embed(title="Weathering Valentines With You", description='', url="", color=0xff69b4)

    # Add author, thumbnail, fields, and footer to the embed
    emb.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://pbs.twimg.com/media/DV7UwvVV4AEKdwH.jpg')
    emb.set_image(url='https://media.giphy.com/media/Vd8tNvUJl2PXZqOPe4/giphy.gif')
    emb.add_field(name="Join me for movie and wine night!", value="It has been a while since our last event, and I figured it would be my turn to plan something this time. I will be hosting the movie in discord while we relax and have a good time. This has been in the works for a little while now, but its finally here. Please react with your availability so we can finalize a time! ", inline=False) 
    emb.add_field(name='Dates:', value='Saturday, Febuary 13 \n Sunday, Febuary 14 \n Friday, Febuary 19 \n Saturday, Febuary 20 \n Sunday, Febuary 21 \n Other  \n 10:00 PM \n 11:00 PM \n 12:00 AM', inline=True)
    emb.add_field(name='Reaction:', value=f'{options[0]} \n {options[1]} \n {options[2]} \n {options[3]} \n {options[4]} \n {options[5]} \n {times[0]} \n {times[1]} \n {times[2]}', inline=True)
    emb.set_footer(text="I know yall are single lonely binches so be there or be square")

    msg = await ctx.send(embed=emb)
    for option in options:
        await msg.add_reaction(option)
    for time in times:
        await msg.add_reaction(time)
    await ctx.message.delete()

@client.command(name='m2')
async def mov2(ctx):
    emb=discord.Embed(title="RSVP: Weathering Valentines With You", description='', url="", color=0xff69b4)

    # Add author, thumbnail, fields, and footer to the embed
    emb.set_author(name=ctx.author.display_name, url="", icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://pbs.twimg.com/media/DV7UwvVV4AEKdwH.jpg')
    emb.set_image(url='https://i.imgur.com/KFjIZee.jpg')
    emb.add_field(name="Saturday, Feb 20 @ 11 PM", value="Please react with a :white_check_mark: to confirm that this time works for you, or comment below. Additionally, please make sure to have **wine and snacks** ready for immediate consumption!", inline=False) 
    emb.set_footer(text="An exciting sneak peek of whats to come")

    msg = await ctx.send(embed=emb)
    await msg.add_reaction('✅')
    await ctx.message.delete()

@client.event
async def on_member_join(member):
    await member.send(f'Welcome to my server {member}!')
    if member.is_on_mobile():
        await member.send(f'You are accessing discord through the mobile UI.')

@client.event
async def on_reaction_add(reaction, user):
    #print("reaction added!")
    pass

@client.event
async def on_raw_reaction_add(payload):
    #print("raw reaction added!")
    await assign_role(payload, True)

@client.event
async def on_raw_reaction_remove(payload):
    #print("raw reaction removed!")
    await assign_role(payload, False)

@client.event
async def on_reaction_remove(reaction, user):
    #print("reaction removed!")
    pass

@client.command(name='reactmode')
async def rctmd(ctx, num:int=1):
    global mode
    mode = num
    await ctx.message.add_reaction('☑️')

@client.event
async def on_message(message):
    # sparkling heart, heartbeat, heart pulse, heart, cupid, two hearts, revolving hearts
    valid_emojis = ['💖', '💓','💗','❤️','💘','💕','💞']
    # defaults to mode 1 if invalid value is passed
    used_emojis = {
        1 : valid_emojis,
        2 : [valid_emojis[ri(0, len(valid_emojis)-1)]],
        3 : valid_emojis[6:7]
    }.get(mode, 1)
    # recursion base case
    if message.author == client.user:
        return
    if message.author.bot:
        if message.embeds:
            if 'Claims: #' in message.embeds[0].description:
                for emoji in used_emojis:
                    await message.add_reaction(emoji)
    await client.process_commands(message)
                
# print(f'author: {emb.author}')
# print(f'desc:   {emb.description}')
# print(f'img:    {emb.image}')
# print(f'title:  {emb.title}')
# print(f'fields: {emb.fields}')
async def assign_role(payload, status):
    if  payload.channel_id != ch_id or payload.message_id != msg_id:
        return

    guild = client.get_guild(payload.guild_id)
    member = get(guild.members, id=payload.user_id)
    role = get(guild.roles, name='user')

    if role is not None:
        if status:
            await member.add_roles(role, reason=f'{member} read the rules.')
            print(f'Assigned {member} to {role}.')
        else:
            await member.remove_roles(role, reason=f'{member} removed their signature.')
            print(f'Removed {member} from {role}.')


#loop = asyncio.get_event_loop()
#loop.run_until_complete(run())
client.run(config['discord']['token'])