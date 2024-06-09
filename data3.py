import gradio as gr
from database import session, Translation

# Function to fetch stored translations from the database
def fetch_translations():
    translations = session.query(Translation).all()
    return translations

# Define the translation interfaces here...

# Define the function for the view translations interface
def view_translations():
    translations = fetch_translations()
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
        # Define your translation interfaces here...
        
        view_translations_interface
    ],
    ["Text Translation", "Voice Command Translation", "Document Translator", "View Translations"]
)

# Launch the Gradio interface
if __name__ == '__main__':
    iface.launch()
