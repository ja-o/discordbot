from discord.ext import commands
from discord_slash import SlashCommand
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, override_type = True)

bot.load_extension("cog")
bot.run(config['discord']['token'])
