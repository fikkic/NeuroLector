from gigachat import GigaChat
from config import GIGACHAT_AUTH
import json

# Инициализация GigaChat
giga = GigaChat(credentials=GIGACHAT_AUTH, verify_ssl_certs=False)

def generate_summary_and_quiz(text: str) -> str:
    prompt = (
        f"Проанализируй следующий текст лекции:\n{text}\n\n"
        f"1. Сделай структурированный конспект (выдели главные темы, определения).\n"
        f"2. Составь 3 вопроса для самопроверки с вариантами ответов (A, B, C) и правильным ответом.\n"
        f"Используй форматирование Markdown."
    )
    try:
        response = giga.chat(prompt)
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка нейросети: {e}"

def extract_graph_data(text: str) -> list:
    """
    Просит нейросеть вернуть связи понятий для Mind Map.
    Ожидаем формат JSON-списка пар.
    """
    prompt = (
        f"Проанализируй текст и выдели 5-8 ключевых логических связей между понятиями для построения ментальной карты.\n"
        f"Текст: {text[:4000]}...\n\n" # Обрезаем, если слишком длинный
        f"Верни ответ ТОЛЬКО в формате JSON списка списков, где первый элемент - понятие, второй - понятие, с которым оно связано.\n"
        f"Пример: [['Нейросеть', 'Обучение'], ['Обучение', 'Данные'], ['Процессор', 'Вычисления']]"
    )
    
    try:
        response = giga.chat(prompt)
        content = response.choices[0].message.content
        
        # Очистка от лишних символов (иногда ИИ пишет ```json ... ```)
        content = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Ошибка парсинга графа: {e}")
        return []