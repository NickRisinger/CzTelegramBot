import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    PATH_FILE_ALLOWED_GTINS: str = os.getenv('PATH_FILE_ALLOWED_GTINS')
    PATH_FILE_PRODUCTS: str = os.getenv('PATH_FILE_PRODUCTS')