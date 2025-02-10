from discord.ext import commands
from repositories.movie_repo import get_movies, get_movie_by_name, create_movie, delete_movie, get_movies_names, update_movie
from utils.helper_functions import check_message, formata_lista
from utils.embeds import send_error_embed, success_embed, info_embed, warning_embed
from utils.pagination_view import PaginationView
from utils.film_selection import FilmSelectionView
from api.movie_api import fetch_movie_data
from sqlalchemy.orm import Session

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

        if get_movie_by_name(movie['title']):
            await ctx.send(embed=send_error_embed(f'O filme {movie_name} já foi adicionado.'))
            return

        if ctx.author.nick:
            nickname = ctx.author.nick
        else:
            nickname = ctx.author.name

        create_movie(name=movie['title'], duration=movie['duracao'], provider=movie['provedores'],
                    rating=movie['rating'], poster_url=movie['poster_url'], added_by=nickname)

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
        movie = get_movie_by_name(movie_name)

        if not movie:
            await ctx.send(embed=send_error_embed(f'Não foi possível deletar o filme {movie_name}, pois ele não foi adicionado.'))
            return
        
        delete_movie(movie)

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
                filme_disponiveis = [filme for filme in movies if filme not in rejeitados]

                if not filme_disponiveis:
                    await ctx.send(embed=send_error_embed('Não há filmes disponíveis para sorteio.'))
                    return

                filme = random.choice(filme_disponiveis)
                info = get_movie_by_name(filme)

                duracao = info.duration
                streamio = info.provider
                poster_url = f"https://image.tmdb.org/t/p/original{info.poster_url}"

                embed_filme = discord.Embed(
                    color=discord.Color.dark_grey(),
                    title='Filme Sorteado'
                )

                embed_filme.set_image(url=poster_url)
                embed_filme.add_field(name='Nome:', value=info.name, inline=False)
                embed_filme.add_field(name='Duração:', value=duracao)
                embed_filme.add_field(name='Onde Passa:', value=streamio)

                await ctx.send(embed=embed_filme)

                view = FilmSelectionView(ctx)
                await ctx.send(embed=info_embed('Deseja selecionar o filme?'), view=view)
                
                await view.wait()

                if view.response:
                    selecionado = True
                    info.viewed = True
                    if not update_movie(info, viewed=True):
                        await ctx.send(embed=send_error_embed('Não foi possível selecionar o filme.'))
                        return
                    
                    await ctx.send(embed=success_embed(f'O filme {info.name} foi selecionado com sucesso!'))
                    return

                elif view.response == False:
                    rejeitados.append(filme)
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
    
    @commands.command(name='selecionar', brief='Seleciona um filme da lista')
    async def selecionar_filme(self, ctx: commands.Context, *, movie_name: str):
        movie = get_movie_by_name(movie_name)

        try:

            if not movie:
                await ctx.send(embed=send_error_embed(f'O filme {movie_name} não foi encontrado.'))
                return
            
            embed_filme = discord.Embed(
                color=discord.Color.dark_grey(),
                title='Filme Escolhido'
            )

            poster_url = f"https://image.tmdb.org/t/p/original{movie.poster_url}"

            embed_filme.set_image(url=poster_url)
            embed_filme.add_field(name='Nome:', value=movie.name, inline=False)
            embed_filme.add_field(name='Duração:', value=movie.duration)
            embed_filme.add_field(name='Onde Passa:', value=movie.provider)
            
            await ctx.send(embed=embed_filme)

            view = FilmSelectionView(ctx)
            await ctx.send(embed=info_embed('Deseja selecionar o filme?'), view=view)
            
            await view.wait()

            if view.response:

                if not update_movie(movie, viewed=True):
                    await ctx.send(embed=send_error_embed('Não foi possível selecionar o filme.'))
                    return
                
                await ctx.send(embed=success_embed(f'O filme {movie.name} foi selecionado com sucesso!'))
                return
            
            else:
                await ctx.send(embed=info_embed(f'O filme {movie.name} não foi selecionado'))
                return
            
        except asyncio.TimeoutError:
            await ctx.send(embed=warning_embed('Tempo esgotado para selecionar o filme.'))
            return

        except Exception as e:
            await ctx.send(embed=send_error_embed(f'Ocorreu um erro ao selecionar o filme'))
            return

async def setup(bot):
    await bot.add_cog(MovieCommands(bot))