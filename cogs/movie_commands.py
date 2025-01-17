from discord.ext import commands
from database import add_movie, get_movies, get_movieid_by_name, delete_movie, update_movie, get_movies_names, get_movie_info
from utils.helper_functions import check_message, formata_lista
from utils.embeds import send_error_embed, success_embed, info_embed, warning_embed
from utils.pagination_view import PaginationView
from utils.film_selection import FilmSelectionView
from api.movie_api import fetch_movie_data

import asyncio
import random
import discord
import time

class MovieCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addfilme', brief='Adiciona um filme à lista de filmes')
    async def add_movie_command(self, ctx: commands.Context, *, movie_name: str):

        movie = fetch_movie_data(movie_name)    

        if 'error' in movie:
            await ctx.send(embed=send_error_embed(f'O filme {movie_name} não foi encontrado.'))
            return
        
        if get_movieid_by_name(movie['title']):
            await ctx.send(embed=send_error_embed(f'O filme {movie_name} já foi adicionado.'))
            return

        if ctx.author.nick:
            nickname = ctx.author.nick
        else:
            nickname = ctx.author.name

        add_movie(movie['title'], movie['tmdb_id'], movie['duracao'], movie['provedores'], movie['rating'], movie['poster_url'], nickname)

        embed_filme = discord.Embed(
            color=discord.Color.dark_green(),
            description='Filme Adicionado com Sucesso'
        )

        embed_filme.set_thumbnail(url=f"https://image.tmdb.org/t/p/original{movie['poster_url']}")
        embed_filme.add_field(name='Nome:', value=movie['title'], inline=False)
        embed_filme.add_field(name='Duração:', value=movie['duracao'])
        embed_filme.add_field(name='Adicionado por:', value=nickname)

        await ctx.send(embed=embed_filme)

    @commands.command(name='listar', brief='Lista todos os filmes adicionados')
    async def listar_filmes(self, ctx: commands.Context):
        movies: list = get_movies()

        if not movies:
            await ctx.send(embed=send_error_embed('Nenhum filme adicionado.'))
            return
        
        pagination_view = PaginationView(movies, ctx)
        await pagination_view.send(ctx)

    @commands.command(name='infofilme', brief='Mostra onde o filme está disponível')
    async def onde_passa_filme(self, ctx: commands.Context, *, movie_name: str):
        movie = fetch_movie_data(movie_name)

        if 'error' in movie:
            await ctx.send(embed=send_error_embed(f'O filme {movie_name} não foi encontrado.'))
            return
        
        embed_filme = discord.Embed(
            color=discord.Color.dark_green(),
            title=f'{movie_name}'
        )

        embed_filme.set_thumbnail(url=f"https://image.tmdb.org/t/p/original{movie['poster_url']}")
        embed_filme.add_field(name='Onde passa:', value=movie['provedores'])
        embed_filme.add_field(name='Duração:', value=movie['duracao'])
        embed_filme.add_field(name='Nota:', value=movie['rating'], inline=False)

        await ctx.send(embed=embed_filme)

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
        rejeitados = []

        try:
            while not selecionado:
                filme_disponiveis = [filme for filme in movies if filme[0] not in rejeitados]

                if not filme_disponiveis:
                    await ctx.send(embed=send_error_embed('Não há filmes disponíveis para sorteio.'))
                    return

                filme = random.choice(filme_disponiveis)
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
                embed_filme.add_field(name='Onde Passa:', value=streamio)

                await ctx.send(embed=embed_filme)

                view = FilmSelectionView(ctx)
                await ctx.send(embed=info_embed('Deseja selecionar o filme?'), view=view)
                
                await view.wait()

                if view.response:
                    selecionado = True
                    if not update_movie(movie_id):
                        await ctx.send(embed=send_error_embed('Não foi possível selecionar o filme.'))
                        return
                    
                    await ctx.send(embed=success_embed(f'O filme {filme[0]} foi selecionado com sucesso!'))
                    return

                elif view.response == False:
                    rejeitados.append(filme[0])
                    await ctx.send(embed=send_error_embed('Filme rejeitado. Sorteando outro filme...'))
                    time.sleep(2)
                else:
                    await ctx.send(embed=send_error_embed('Erro ao selecionar o filme.'))
                    return
                
        except asyncio.TimeoutError:
            await ctx.send(embed=warning_embed('Tempo esgotado para selecionar o filme.'))
            return

        except Exception as e:
            await ctx.send(embed=send_error_embed(f'Ocorreu um erro: {str(e)}'))
            return
    
async def setup(bot):
    await bot.add_cog(MovieCommands(bot))