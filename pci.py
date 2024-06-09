import gradio as gr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from fpdf import FPDF
from database import session, Translation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

class PDF(FPDF):
    def header(self):
        self.add_font('NotoSans', '', 'NotoSans-VariableFont_wdth,wght.ttf', uni=True)
        self.set_font('NotoSans', '', 12)
        self.cell(0, 10, 'Translated Document', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('NotoSans', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def translate_text_googletrans(text, targ_lang):
    if not targ_lang:
        raise ValueError("Target language must be specified.")

    translator = GoogleTranslator(target=targ_lang)
    translated_text = ""
    chunk_size = 1000

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        translated_chunk = translator.translate(text=chunk)
        translated_text += translated_chunk + ' '

    return translated_text

def register_fonts():
    font_files = {
        'NotoSans': 'NotoSans-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Bengali': 'NotoSansBengali-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Devanagari': 'NotoSansDevanagari-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Kannada': 'NotoSansKannada-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Malayalam': 'NotoSansMalayalam-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Tamil': 'NotoSansTamil-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Telugu': 'NotoSansTelugu-VariableFont_wdth,wght.ttf'
    }
    
    for font_name, font_file in font_files.items():
        if not os.path.exists(font_file):
            raise FileNotFoundError(f"Font file '{font_file}' not found. Please ensure it is in the correct directory.")
        pdfmetrics.registerFont(TTFont(font_name, font_file))

def create_pdf(text):
    pdf = PDF()
    pdf.add_page()

    # Registering fonts for FPDF
    font_files = {
        'NotoSans': 'NotoSans-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Bengali': 'NotoSansBengali-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Devanagari': 'NotoSansDevanagari-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Kannada': 'NotoSansKannada-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Malayalam': 'NotoSansMalayalam-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Tamil': 'NotoSansTamil-VariableFont_wdth,wght.ttf',
        'Noto_Sans_Telugu': 'NotoSansTelugu-VariableFont_wdth,wght.ttf'
    }
    
    for font_name, font_file in font_files.items():
        pdf.add_font(font_name, '', font_file, uni=True)

    # Splitting text into lines to fit within the page width
    lines = text.split('\n')
    max_lines = 50  # You can adjust this as needed
    lines = lines[:max_lines]  # Limiting to a maximum number of lines

    # Selecting font based on language
    for line in lines:
        if is_bengali(line):
            pdf.set_font('Noto_Sans_Bengali', '', 12)
        elif is_devanagari(line):
            pdf.set_font('Noto_Sans_Devanagari', '', 12)
        elif is_kannada(line):
            pdf.set_font('Noto_Sans_Kannada', '', 12)
        elif is_malayalam(line):
            pdf.set_font('Noto_Sans_Malayalam', '', 12)
        elif is_tamil(line):
            pdf.set_font('Noto_Sans_Tamil', '', 12)
        elif is_telugu(line):
            pdf.set_font('Noto_Sans_Telugu', '', 12)
        else:
            pdf.set_font('NotoSans', '', 12)
        pdf.cell(0, 10, txt=line, ln=True)

    pdf_file = "translated_document.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Utility functions to detect script based on Unicode range
def is_bengali(text):
    for char in text:
        if '\u0980' <= char <= '\u09FF':
            return True
    return False

def is_devanagari(text):
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return True
    return False

def is_kannada(text):
    for char in text:
        if '\u0C80' <= char <= '\u0CFF':
            return True
    return False

def is_malayalam(text):
    for char in text:
        if '\u0D00' <= char <= '\u0D7F':
            return True
    return False

def is_tamil(text):
    for char in text:
        if '\u0B80' <= char <= '\u0BFF':
            return True
    return False

def is_telugu(text):
    for char in text:
        if '\u0C00' <= char <= '\u0C7F':
            return True
    return False

# Register the fonts once before creating the PDF
register_fonts()

def translate_pdf(file, targ_lang):
    text = extract_text_from_pdf(file.name)
    translated_text = translate_text_googletrans(text, targ_lang)

    # Save the translation to the database
    new_translation = Translation(
        source_text=text,
        translated_text=translated_text,
        source_language='auto',
        target_language=targ_lang
    )
    session.add(new_translation)
    session.commit()

    pdf_file = create_pdf(translated_text)
    return translated_text, pdf_file

def document_translation_interface(file, targ_lang):
    translated_text, pdf_file = translate_pdf(file, targ_lang)
    return translated_text, pdf_file

def get_supported_languages():
    languages = GoogleTranslator().get_supported_languages()
    return languages


def document_translation_interface_gradio():
    uploaded_file = gr.File(label="Upload PDF file")
    targ_lang = gr.Dropdown(
        label="Please choose translation language from list:",
        choices=list(get_supported_languages()),
    )
    translate_button = gr.Button("Translate")
    extracted_text_output = gr.Textbox(label="Extracted and Translated Text")
    translated_pdf_output = gr.File(label="Download Translated PDF")

    return gr.Interface(
        fn=document_translation_interface,
        inputs=[uploaded_file, targ_lang],
        outputs=[extracted_text_output, translated_pdf_output],
        title='PDF Translator',
        description='Translate PDF files from one language to another and download the translated document.'
    )


if __name__ == '__main__':
    document_translation_interface_gradio().launch()
