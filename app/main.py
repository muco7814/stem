from app.ui.interface import build_interface
import gradio as gr
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

CUSTOM_CSS = """
.app-container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.title-banner { text-align: center; }
"""

demo = build_interface()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        share=False,
        theme=gr.themes.Soft(),  # Moved here
        css=CUSTOM_CSS           # Moved here
    )