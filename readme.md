# Discord Movie Bot

Um bot do Discord para gerenciamento de uma lista de filmes, permitindo adicionar, sortear e selecionar filmes para assistir.

## How to download it

- Clone o repositório

    ```bash
    https://github.com/thiagcarvalho/movie-mate.git
    cd movie-mate
    ```
- Crie o discord bot [aqui](https://discord.com/developers/applications)
- Colete o bot token
- Convide o bot para seu servidor
    - Use o seguinte link substituindo `YOUR_APPLICATION_ID_HERE` pelo ID do seu aplicativo e `PERMISSIONS` pelas permissões necessárias:

    
    ```bash
    https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS
    
    ```

    - Para encontrar o ID do bot, acesse a aba **General Information** dentro do Discord Developer Portal.

## Como configurar o Bot

### `.env` file

Para configurar o token você terar que usar o arquivo `.env_example`, você deve **renomea-lo** para `.env` e alterar o valor dos seguintes valores:

#### `DISCORD_TOKEN`

Insira o valor do token obtido no momento da criação do bot.

#### `URL_DATABASE`

O bot suporta diferentes bancos de dados, pois utiliza SQLAlchemy. Defina a string de conexão conforme o banco escolhido.

* Exemplos para PostgreSQL:

    ```
    DATABASE_URL=postgresql://user:password@localhost:5432/database_name
    ```

* Exemplo para SQLite:
    ```
    DATABASE_URL=sqlite:///database.db
    ```

#### TMDB API ou `API_KEY`
O bot utiliza a base de dados do TMDB. Para isso, é necessário criar uma conta no  [The Movie Database](https://developer.themoviedb.org/reference/intro/getting-started) e obter um token de API. Após criar a conta, adicione o token ao arquivo `.env`:

    API_KEY=sua_chave_aqui
    

## Como iniciar o Bot

Antes de executar o bot, instale todas as dependências:
```bash
pip install -r requirements.txt
```

Depois disso, inicie o bot com o comando abaixo:
```bash
python3 bot.py
```

> **Nota:** O comando pode variar dependendo da sua instalação do Python (`python`, `python3`, `py`, etc.).

## Built With

* Python 3.9.13


