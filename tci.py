import gradio as gr
from deep_translator import GoogleTranslator
from database import session, Translation

def translate_text(input_text, target_language):
    if not target_language:
        raise ValueError("Target language must be specified.")
     # Debug statement
    translator = GoogleTranslator(target=target_language)
    translated = translator.translate(text=input_text)
     # Debug statement

    # Save the translation to the database
    new_translation = Translation(
        source_text=input_text,
        translated_text=translated,
        source_language='auto',
        target_language=target_language
    )
    session.add(new_translation)
    session.commit()

    return translated

def text_translation_interface(input_text, target_language):
    inp = input_text
    tr = target_language
    translated = translate_text(inp, tr)
    return translated

def get_supported_languages():
    return GoogleTranslator().get_supported_languages()

def text_translation_interface_gradio():
    supported_languages = get_supported_languages()
    language_choices = list(supported_languages)  # Ensure correct format
   # Debug statement

    input_text = gr.Textbox(label="Enter Text")
    target_language = gr.Dropdown(label="Choose Language", choices=language_choices)
    output_text = gr.Textbox(label="Translated Text")
    translate_button = gr.Button("Translate")

    def on_translate(input_text, target_language):
        return text_translation_interface(input_text, target_language)

    return gr.Interface(
        fn=on_translate,
        inputs=[input_text, target_language],
        outputs=output_text,
        title="Text Translator",
        description="Translate text from one language to another."
    )
if __name__ == '__main__':
    text_translation_interface_gradio().launch()
