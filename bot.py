import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import Base, engine
from models.movie import Movie
import os

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

Base.metadata.create_all(bind=engine)
#intents controlam quais eventos o bot pode ter acesso (mensagens, reações, etc)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='f!', intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension('cogs.movie_commands')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title='Comando não encontrado',
            description='Use f!help para ver os comandos disponíveis.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)