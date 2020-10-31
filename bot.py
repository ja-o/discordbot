import os
import json
import configparser
import discord
from discord.utils import get
from discord.ext import commands
from discord import Intents

config = configparser.ConfigParser()
config.read('config.ini')
intents_all = Intents.all()
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="$", intents=intents_all)
ch_id = config['discord']['ch_id']
msg_id = config['discord']['msg_id']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #ch = client.get_channel(ch_id)
    await client.change_presence(activity=discord.Game(name='Exploring the 「Library」'))

@client.command(name="hello")
async def hello(ctx):
    await ctx.send("Hi, how are you doing today?")
    await ctx.send(ctx)

@client.command(name="kellyn")
async def kellyn(ctx):
    await ctx.send("!hello, how are you doing today Haro?")

@client.event
async def on_member_join(member):
    await member.send(f'Welcome to my server {member}!')
    if member.is_on_mobile():
        await member.send(f'You are accessing discord through the mobile UI.')

@client.event
async def on_reaction_add(reaction, user):
    print("reaction added!")

@client.event
async def on_raw_reaction_add(payload):
    print("raw reaction added!")
    print(payload)
    await assign_role(payload, True)

@client.event
async def on_raw_reaction_remove(payload):
    print("raw reaction removed!")
    await assign_role(payload, False)

@client.event
async def on_reaction_remove(reaction, user):
    print("reaction removed!")

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


client.run(config['discord']['token'])
