from fpdf import FPDF
import os
from config import OUTPUTS_DIR, FONTS_DIR

class LecturePDF(FPDF):
    def header(self):
        self.set_font('DejaVu', '', 10)
        self.cell(0, 10, 'NeuroLector - Автоматический конспект', align='R', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

def create_pdf(text: str, image_path: str, file_id: str) -> str:
    pdf = LecturePDF()
    
    # Регистрация русского шрифта
    font_path = os.path.join(FONTS_DIR, "DejaVuSans.ttf")
    if os.path.exists(font_path):
        pdf.add_font('DejaVu', '', font_path)
        pdf.set_font('DejaVu', '', 12)
    else:
        # Fallback (русский не будет работать корректно без шрифта)
        pdf.set_font("Arial", size=12) 
        print("ВНИМАНИЕ: Шрифт не найден, русский текст может не отобразиться!")

    pdf.add_page()
    
    # Заголовок
    pdf.set_font_size(16)
    pdf.cell(0, 10, "Конспект лекции", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Текст конспекта
    pdf.set_font_size(11)
    # FPDF2 multi_cell корректно переносит строки
    pdf.multi_cell(0, 8, text)
    pdf.ln(10)
    
    # Вставка Mind Map
    if image_path and os.path.exists(image_path):
        pdf.add_page()
        pdf.set_font_size(14)
        pdf.cell(0, 10, "Ментальная карта (Mind Map)", new_x="LMARGIN", new_y="NEXT")
        pdf.image(image_path, x=10, y=30, w=190)

    output_filename = os.path.join(OUTPUTS_DIR, f"notes_{file_id}.pdf")
    pdf.output(output_filename)
    return output_filename