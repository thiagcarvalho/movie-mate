from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle
from database import add_movie, get_movies, get_movieid_by_name, delete_movie, update_movie, get_movies_names, get_movie_info
from utils.helper_functions import check_message, formata_lista, valida_nome
from utils.embeds import send_error_embed, success_embed, info_embed, warning_embed
from api.movie_api import fetch_movie_data

import asyncio
import random
import discord

class MovieCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addfilme', brief='Adiciona um filme à lista de filmes')
    async def add_movie_command(self, ctx: commands.Context, *, movie_name: str):

        if not valida_nome(movie_name):
            await ctx.send(embed=warning_embed('Nome do filme deve conter apenas letras e números.'))
            return
        
        if get_movieid_by_name(movie_name):
            await ctx.send(embed=send_error_embed(f'O filme {movie_name} já foi adicionado.'))
            return

        movie = fetch_movie_data(movie_name)    

        if 'error' in movie:
            await ctx.send(embed=send_error_embed(f'O filme {movie_name} não foi encontrado.'))
            return

        if ctx.author.nick:
            nickname = ctx.author.nick
        else:
            nickname = ctx.author.name

        add_movie(movie_name, movie['tmdb_id'], movie['duracao'], movie['provedores'], movie['rating'], movie['poster_url'], nickname)

        embed_filme = discord.Embed(
            color=discord.Color.dark_green(),
            description='Filme Adicionado com Sucesso'
        )

        embed_filme.set_thumbnail(url=f"https://image.tmdb.org/t/p/original{movie['poster_url']}")
        embed_filme.add_field(name='Nome:', value=movie_name, inline=False)
        embed_filme.add_field(name='Duração:', value=movie['duracao'])
        embed_filme.add_field(name='Adicionado por:', value=nickname)

        await ctx.send(embed=embed_filme)

    @commands.command(name='listar', brief='Lista todos os filmes adicionados')
    async def listar_filmes(self, ctx: commands.Context):
        movies: list = get_movies()

        if not movies:
            await ctx.send(embed=send_error_embed('Nenhum filme adicionado.'))
            return
        
        cabecalho = ['Nome', 'Duração', 'Onde Passa', 'Nota']
        tabela = t2a(
            header=cabecalho, 
            body=movies, 
            style=PresetStyle.thin,
            first_col_heading=True
        )

        await ctx.send(f'🎬 Filmes Adicionados: ```\n{tabela}\n```')

    @commands.command(name='deletar', brief='Deleta um filme da lista')
    async def deletar_filme(self, ctx: commands.Context, *, movie_name: str):
        movie_id = get_movieid_by_name(movie_name)

        if not movie_id:
            await ctx.send(embed=send_error_embed(f'Não foi possível deletar o filme {movie_name}, pois ele não foi adicionado.'))
            return
        
        delete = delete_movie(movie_id)

        await ctx.send(embed=success_embed(f'O filme {movie_name} foi deletado com sucesso!'))

    @commands.command(name='sortear', brief='Sorteia um filme da lista')
    async def sortear_filme(self, ctx: commands.Context):
        movies: list = get_movies_names()

        if not movies:
            await ctx.send(embed=send_error_embed('Nenhum filme adicionado.'))
            return
        
        selecionado = False

        try:
            while selecionado != True:
                filme = random.choice(movies)
                info = get_movie_info(filme[0])[0]
                
                duracao = info[0]
                streamio = info[1]
                poster_url = f"https://image.tmdb.org/t/p/original{info[2]}"
                movie_id = int(info[3])

                embed_filme = discord.Embed(
                    color=discord.Color.dark_grey(),
                    title='Filme Sorteado'
                )

                embed_filme.set_image(url=poster_url)
                embed_filme.add_field(name='Nome:', value=filme[0], inline=False)
                embed_filme.add_field(name='Duração:', value=duracao)
                embed_filme.add_field(name='Streamio:', value=streamio)


                await ctx.send(embed=embed_filme)

                await ctx.send(embed=info_embed('Deseja selecionar o filme? (sim/nao)'))

                msg = await self.bot.wait_for('message', timeout=40, 
                                            check=lambda message: check_message(message, ctx.author, ctx.channel))

                if msg.content.lower() == 'sim':
                    selecionado = True
                    
                    if not update_movie(movie_id):
                        await ctx.send(embed=send_error_embed('Não foi possível selecionar o filme.'))
                        return

                    await ctx.send(embed=success_embed('Filme selecionado com sucesso!'))
                    return 

        except asyncio.TimeoutError:
            await ctx.send(embed=warning_embed('Tempo esgotado para selecionar o filme.'))
            return

        except Exception as e:
            await ctx.send(embed=send_error_embed(f'Ocorreu um erro: {str(e)}'))
            return
    
async def setup(bot):
    await bot.add_cog(MovieCommands(bot))