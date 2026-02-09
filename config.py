import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GIGACHAT_AUTH = os.getenv("GIGACHAT_AUTH")

# Пути к папкам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

# Создаем папки, если их нет
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)