import asyncio
import logging
import os
import sys
import shutil


try:
    import imageio_ffmpeg
    # Получаем скачанный файл (со странным именем)
    ffmpeg_original = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Определяем папку Scripts внутри твоего .venv (где лежит python.exe)
    venv_scripts_dir = os.path.dirname(sys.executable)
    
    # Путь, где Whisper ожидает найти файл
    ffmpeg_dest = os.path.join(venv_scripts_dir, "ffmpeg.exe")
    
    # Если правильного файла еще нет, копируем и переименовываем!
    if not os.path.exists(ffmpeg_dest):
        shutil.copy(ffmpeg_original, ffmpeg_dest)
        print(f"✅ FFmpeg успешно скопирован и переименован в: {ffmpeg_dest}")
except Exception as e:
    print(f"⚠️ Ошибка при настройке FFmpeg: {e}")


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession 

from config import BOT_TOKEN
from handlers import user

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    session = AiohttpSession(timeout=1200)

    bot = Bot(
        token=BOT_TOKEN, 
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    dp.include_router(user.router)
    
    print("🧹 Очистка старых сообщений...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🚀 NeuroLector запущен! (FFmpeg установлен как надо)")
    
    await dp.start_polling(bot, polling_timeout=60)

if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")