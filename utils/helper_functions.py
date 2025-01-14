from discord import Message, TextChannel, User

import re

#Basica compara se o autor da mensagem é o mesmo que o autor da mensagem que o bot está esperando
def check_message(message: Message, author: User, channel: TextChannel) -> bool:
    return message.author == author and message.channel == channel

def formata_lista(movies: list) -> str:
    """
    Formata lista de filmes para ser enviada no chat
    """
    if not movies:
        return 'Nenhum filme encontrado.'
    
    movie_names = [movie[0] for movie in movies]
    return f'{", ".join(movie_names)}'
