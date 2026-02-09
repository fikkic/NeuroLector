import whisper
import os

# Загружаем модель один раз при старте (base - баланс скорости и качества)
model = whisper.load_model("base")

async def transcribe_audio(file_path: str) -> str:
    """
    Принимает путь к аудиофайлу, возвращает текст.
    """
    try:
        # Whisper работает синхронно, но для MVP это нормально.
        # В продакшене это запускают в отдельном потоке (executor).
        result = model.transcribe(file_path, language="ru")
        return result["text"]
    except Exception as e:
        print(f"Ошибка транскрибации: {e}")
        return ""