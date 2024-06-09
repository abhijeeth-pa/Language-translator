import os
import gradio as gr
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import pygame
import warnings
from tempfile import NamedTemporaryFile
import soundfile as sf

warnings.filterwarnings("ignore", category=UserWarning)
pygame.mixer.init()

def translate_audio(audio_data, sampling_rate, target_lang):
    recognizer = sr.Recognizer()
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        sf.write(temp_audio, audio_data, sampling_rate)
        temp_audio.flush()
        temp_audio.seek(0)
        
        with sr.AudioFile(temp_audio.name) as source:
            audio = recognizer.record(source)
    
    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"Recognized text: '{text}'")

        # Translate the recognized text
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(text=text)
        print(f"Translated text: '{translated_text}'")
        
        # Convert translated text to speech
        tts = gTTS(text=translated_text, lang=target_lang)
        temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        
        return translated_text, temp_file.name

    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio.", None
    except sr.RequestError as e:
        return f"Could not request results; {e}", None

def speak_translation(mp3_path):
    if mp3_path:
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()

def get_supported_languages():
    return GoogleTranslator().get_supported_languages(as_dict=True)

def voice_translation_interface():
    with gr.Blocks() as demo:
        audio_input = gr.Audio(label="Upload Recording")
        target_lang = gr.Dropdown(
            label="Target Language",
            choices=list(get_supported_languages().values()),
            value="en"  # Default value set to English
        )
        translate_button = gr.Button("Translate")
        speak_button = gr.Button("Speak Out")
        download_button = gr.Button("Download Translation")
        translated_text_output = gr.Textbox(label="Translated Text")
        download_link = gr.File(label="Download MP3")

        def translate_and_speak(audio, target_lang):
            sampling_rate, audio_data = audio  # Unpack the tuple
            translated_text, mp3_path = translate_audio(audio_data, sampling_rate, target_lang)
            return translated_text, mp3_path, mp3_path

        translate_button.click(
            translate_and_speak, 
            inputs=[audio_input, target_lang], 
            outputs=[translated_text_output, download_link, gr.State()]
        )
        speak_button.click(
            speak_translation, 
            inputs=gr.State(),
            outputs=None
        )

    return demo

if __name__ == '__main__':
    voice_translation_interface().launch(share=True)
