import requests
import os

TMDB_API_KEY = os.getenv('API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3/'


def search_movie(movie_name: str) -> dict:

    url = f"{TMDB_BASE_URL}/search/movie?query={movie_name}&include_adult=false&language=pt-BR"

    headers = {
        "accept": "application/json", 
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    print(response)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]
        
        return {"error": "Nenhum filme encontrado"}
    return {"error": "Falha ao procurar o filme"}

def get_movie_details(movie_id: int) -> dict:

    url = f"{TMDB_BASE_URL}/movie/{movie_id}?language=pt-BR"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        if dados:
            duration_hours = dados['runtime'] // 60
            duration_minutes = dados['runtime'] % 60
            formatted_duration = f"{duration_hours}h:{duration_minutes}min"
            dados['runtime'] = formatted_duration

            return {
                "title": dados.get('title'),
                "tmdb_id": dados.get('id'),
                "duracao": dados.get('runtime'),
                "rating": dados.get('vote_average'),
                "poster_url": dados.get('poster_path')
            }
    
    return {"error": "Falha ao buscar detalhes do filme"}

def get_movie_provider(movie_id: int) -> list:

    url = f"{TMDB_BASE_URL}/movie/{movie_id}/watch/providers"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    try:
        if response.status_code == 200:
            #essa parte ele pega os provedores de stream do filme
            data = response.json().get('results', {}).get('BR', {})['flatrate']

            if data:
                provedores = []
                for provider in data:
                    provedores.append(provider['provider_name'])

                provedores = ", ".join(provedores[:3])
                return provedores
            
            return ["Nenhum provedor encontrado no Brasil"]

        return ["Falha ao buscar provedores do filme"]
    
    except KeyError:
        return "Streamio"

def fetch_movie_data(movie_name: str) -> dict:

    movie = search_movie(movie_name)
    
    print(movie)
    if "error" in movie:
        return movie
    
    movie_id = movie.get('id')
    movie_details = get_movie_details(movie_id)
    movie_providers = get_movie_provider(movie_id)

    return {
        "title": movie_details.get('title'),
        "tmdb_id": movie_details.get('tmdb_id'),
        "duracao": movie_details.get('duracao'),
        "provedores": movie_providers,
        "rating": movie_details.get('rating'),
        "poster_url": movie_details.get('poster_url')
    }
