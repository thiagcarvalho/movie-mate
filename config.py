import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    DATABASE_URL = os.getenv('URL_DATABASE')
    BOT_TOKEN = os.getenv('BOT_TOKEN')


