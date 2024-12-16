import discord

def send_error_embed(message: str):
    embed_error = discord.Embed(
        description=message,
        color=discord.Color.dark_red()
    )

    return embed_error

def success_embed(message: str):
    embed_success = discord.Embed(
        description=message,
        color=discord.Color.dark_green()
    )

    return embed_success

def info_embed(message: str):
    embed_info = discord.Embed(
        description=message,
        color=discord.Color.dark_grey()
    )

    return embed_info

def warning_embed(message: str):
    embed_warning = discord.Embed(
        description=message,
        color=discord.Color.dark_gold()
    )

    return embed_warning