import gradio as gr
from database import session, Translation
from pro6 import *

# Define the translation interfaces here...
text_translation_interface = gr.Interface(
    fn=text_translation_interface,
    inputs=[
        gr.Textbox(label="Enter Text"),
        gr.Dropdown(label="Choose Language", choices=GoogleTranslator().get_supported_languages(as_dict=True).values())
    ],
    outputs=gr.Textbox(label="Translated Text"),
    title="Text Translator",
    description="Translate text from one language to another."
)

voice_command_interface = gr.Interface(
    fn=voice_command_interface,
    inputs=[
        gr.Dropdown(label="Choose Language", choices=GoogleTranslator().get_supported_languages(as_dict=True).values())
    ],
    outputs=[
        gr.Textbox(label="Recognized Speech"),
        gr.Textbox(label="Translated Text")
    ],
    title="Voice Command Translator",
    description="Translate spoken words from one language to another."
)

textdoc_translation_interface = gr.Interface(
    fn=extract_and_translate_text,
    inputs=[
        gr.Textbox(label='Enter a PDF or TXT file path from your local drive or "Paste" in a sentence...'),
        gr.Slider(label='Start page (PDF only)', minimum=0, maximum=100, step=1, value=0),
        gr.Slider(label='End page (PDF only)', minimum=0, maximum=100, step=1, value=0),
        gr.Dropdown(label='Please choose translation language from list:', choices=GoogleTranslator().get_supported_languages(as_dict=True).values(), value='English'),
        gr.Checkbox(label="Would you like to download the translation?", value=False),
        gr.Textbox(label='Would you like to add a prefix to the file(s)', value="")
    ],
    outputs=[
        gr.Textbox(label='Extracted and Translated Text')
    ],
    title='💥PDF/Text Translator 💥',
    description='Extract and translate from PDF or TXT files as well as a cut and paste snippet.',
    allow_flagging=False,
    examples=[
        ['example.pdf', 1, 1, 'French', False, '']
    ],
)

# Define the view_translations function
def view_translations():
    translations = session.query(Translation).all()
    result = ""
    for translation in translations:
        result += f"ID: {translation.id}\n"
        result += f"Source Text: {translation.source_text}\n"
        result += f"Translated Text: {translation.translated_text}\n"
        result += f"Source Language: {translation.source_language}\n"
        result += f"Target Language: {translation.target_language}\n"
        result += f"Timestamp: {translation.timestamp}\n"
        result += "-" * 20 + "\n"
    return result

# Define the Gradio interface to view translations
view_translations_interface = gr.Interface(
    fn=view_translations,
    inputs=[],
    outputs="textbox",
    title="View Stored Translations",
    description="Display all translations stored in the database."
)

# Define the Gradio tabbed interface
iface = gr.TabbedInterface(
    [
        text_translation_interface,
        voice_command_interface,
        textdoc_translation_interface,
        view_translations_interface
    ],
    ["Text Translation", "Voice Command Translation", "Document Translator", "View Translations"]
)

# Launch the Gradio interface
if __name__ == '__main__':
    iface.launch()
