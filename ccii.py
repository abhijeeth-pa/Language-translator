# main.py
import gradio as gr
import vci  # Importing voice command interface
import pci  # Importing PDF command interface
import tci  # Importing text command interface

# Create a function to launch all interfaces
def launch_all_interfaces():
    with gr.Blocks() as demo:
        gr.Markdown("# Multi-Functional Translator")

        with gr.Tabs():
            with gr.TabItem("Overview and Help"):
                gr.Markdown("""
                ## Project Overview
                This project provides multiple translation services:
                - **Text Translation**: Translate text from one language to another.
                - **Voice Command Translation**: Record speech, translate it, and speak out the translation.
                - **PDF Translation**: Upload PDF files to translate their content and download the translated document.

                ### Help
                - **Text Translation**: Enter the text and select the target language to get the translation.
                - **Voice Command Translation**: Click on "Start Recording", speak, then click "Stop Recording" to get the translation. You can also have the translation spoken out.
                - **PDF Translation**: Upload a PDF file and select the target language to translate the text and download the translated PDF.

                ### Feedback
                We value your feedback. Please provide your suggestions or report any issues below:
                """)

                feedback_text = gr.Textbox(label="Your Feedback", placeholder="Enter your feedback here...")
                submit_button = gr.Button("Submit Feedback")

                def submit_feedback(feedback):
                    with open("feedback.txt", "a") as f:
                        f.write(feedback + "\n")
                    return "Thank you for your feedback!"

                submit_button.click(submit_feedback, inputs=feedback_text, outputs=gr.Textbox(label="", value="Thank you for your feedback!"))

            with gr.TabItem("Text Translation"):
                tci.text_translation_interface_gradio()  # Remove .render()
            
            with gr.TabItem("Voice Command Translation"):
                vci.voice_translation_interface()  # Remove .render()
            
            with gr.TabItem("PDF Translation"):
                pci.document_translation_interface_gradio()  # Remove .render()

    demo.launch()

if __name__ == '__main__':
    launch_all_interfaces()
