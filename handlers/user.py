import os
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from config import DOWNLOADS_DIR
from services.transcriber import transcribe_audio
from services.llm_engine import generate_summary_and_quiz, extract_graph_data
from services.graph_builder import create_mind_map
from services.pdf_maker import create_pdf

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я **NeuroLector**.\n"
        "Отправь мне голосовое сообщение или аудиофайл лекции.\n"
        "Я сделаю конспект, тест и ментальную карту!"
    )

@router.message(F.voice | F.audio)
async def process_audio_message(message: types.Message, bot: Bot):
    status_msg = await message.answer("🎧 Скачиваю аудио...")
    
    # 1. Скачивание
    file_id = message.voice.file_id if message.voice else message.audio.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    local_filename = f"{file_id}.ogg" # Телеграм обычно отдает ogg или mp3
    save_path = os.path.join(DOWNLOADS_DIR, local_filename)
    
    await bot.download_file(file_path, save_path)
    
    # 2. Транскрибация
    await status_msg.edit_text("🧠 Распознаю речь (это может занять время)...")
    text = await transcribe_audio(save_path)
    
    if not text:
        await status_msg.edit_text("❌ Не удалось распознать речь. Возможно, файл пустой или слишком тихий.")
        return

    # 3. Работа ИИ (Конспект)
    await status_msg.edit_text("📝 Пишу конспект и составляю тест...")
    summary = generate_summary_and_quiz(text)
    
    # Отправка текста в чат (обрезаем, если длинный)
    if len(summary) > 4000:
        await message.answer(summary[:4000] + "...")
    else:
        await message.answer(summary, parse_mode="Markdown")

    # 4. Ментальная карта (Mind Map)
    await status_msg.edit_text("🎨 Рисую ментальную карту...")
    graph_data = extract_graph_data(text)
    map_image_path = None
    
    if graph_data:
        map_image_path = create_mind_map(graph_data, file_id)
        if map_image_path:
            photo = FSInputFile(map_image_path)
            await message.answer_photo(photo, caption="🧠 Ваша ментальная карта связей")

    # 5. Генерация PDF
    await status_msg.edit_text("📄 Верстаю PDF...")
    pdf_path = create_pdf(summary, map_image_path, file_id)
    
    if pdf_path:
        doc = FSInputFile(pdf_path)
        await message.answer_document(doc, caption="Вот полный отчет по лекции!")
    
    await status_msg.delete()
    
    # Чистка временных файлов (опционально)
    try:
        os.remove(save_path)
        if map_image_path: os.remove(map_image_path)
        # pdf оставляем или удаляем по желанию
    except:
        pass