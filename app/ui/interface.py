import gradio as gr
import os
from app.core.pipeline import process_audio_pipeline

# Configuration Guards
MAX_FILE_SIZE_MB = 30
ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.m4a']

def validate_and_process(audio_path):
    if not audio_path:
        return [gr.update(value=None)] * 4 + [gr.update(visible=False)]
    
    # Execute backend pipeline
    stems = process_audio_pipeline(audio_path)
    
    # 🚨 DEBUG PRINT 1: What did the backend actually return?
    print("\n" + "="*50)
    print("DEBUG 1 - RAW DICTIONARY FROM BACKEND:")
    print(stems)
    print("="*50 + "\n")
    
    # Safely extract the 4 known outputs by matching dictionary keys
    vocals_path, drums_path, bass_path, other_path = None, None, None, None
    for key, path in stems.items():
        k = path.split('/')[-1]
        if k == 'vocals_normalized.wav':
            vocals_path = path
        elif k == 'drums.wav':
            drums_path = path
        elif k == 'bass.wav':
            bass_path = path
        elif k == 'other.wav':
            other_path = path

    # 🚨 DEBUG PRINT 2: Did the UI successfully map them?
    print("\n" + "="*50)
    print("DEBUG 2 - MAPPED PATHS FOR UI:")
    print(f"Bass:   {bass_path}")
    print(f"Drums:  {drums_path}")
    print(f"Other:  {other_path}")
    print(f"Vocals: {vocals_path}")
    print("="*50 + "\n")

    return [
        gr.update(value=bass_path),
        gr.update(value=drums_path),
        gr.update(value=other_path),
        gr.update(value=vocals_path),
        gr.update(visible=False)  
    ]

def clear_all():
    """Brings the UI back to its base configuration state."""
    return [
        gr.update(value=None),                # bass
        gr.update(value=None),                # drums
        gr.update(value=None),                # other
        gr.update(value=None),                # vocals
        gr.update(value=None),                # input audio
        gr.update(interactive=False),         # submit button
        gr.update(visible=False)              # status label
    ]

def show_loading():
    """Show loading indicators when processing starts"""
    return [
        gr.update(value=None),
        gr.update(value=None),
        gr.update(value=None),
        gr.update(value=None),
        gr.update(visible=True, value="⏳ Processing... This may take a few minutes.") # status
    ]

def build_interface():
    with gr.Blocks(elem_classes="app-container") as demo:
        
        # Header Title Grouping
        gr.Markdown("# AI Audio Stem Separation & Enhancement Engine", elem_classes="title-banner")
        gr.Markdown("Isolate clean, distinct, performance-optimized musical layers instantly.", elem_classes="title-banner")
        
        with gr.Row(equal_height=False):
            # LEFT COLUMN (Smaller footprint: Input Control Interface)
            with gr.Column(scale=2):
                gr.Markdown("### 🎛️ Input Controller")
                input_audio = gr.Audio(
                    type="filepath", 
                    label="Upload Audio Mix Track",
                    sources=["upload"]
                )
                
                with gr.Row():
                    submit_btn = gr.Button("Separate & Enhance", variant="primary", interactive=False)
                    clear_btn = gr.Button("Add New / Clear", variant="stop")
                
                gr.Markdown(f"**System Limits:** Max {MAX_FILE_SIZE_MB}MB | Format: WAV, MP3, FLAC, M4A")
                
                # Loading Status Indicator
                status_label = gr.Label(
                    value="Ready",
                    label="Processing Status",
                    visible=False
                )

            # SPACER INTERSTICE (Visual Padding Division)
            with gr.Column(scale=1):
                gr.Markdown(" ")

            # RIGHT COLUMN (Larger footprint: Performance Stem Arrays)
            with gr.Column(scale=4):
                gr.Markdown("### 🔊 Enhanced Stem Multi-Tracks")
                
                # REMOVED `visible=False` - They now start visible but empty
                bass_out = gr.Audio(label="Isolated Component: BASS", type="filepath", interactive=False)
                drums_out = gr.Audio(label="Isolated Component: DRUMS", type="filepath", interactive=False)
                other_out = gr.Audio(label="Isolated Component: OTHER", type="filepath", interactive=False)
                vocals_out = gr.Audio(label="Isolated Component: VOCALS", type="filepath", interactive=False)
                
                # Array mapped directly to the outputs of our click events
                audio_slots = [bass_out, drums_out, other_out, vocals_out]

        # --- EVENT LISTENERS ---
        input_audio.change(
            fn=lambda audio: gr.update(interactive=True) if audio is not None else gr.update(interactive=False),
            inputs=[input_audio],
            outputs=[submit_btn]
        )

        submit_btn.click(
            fn=show_loading,
            inputs=[],
            outputs=audio_slots + [status_label]
        ).then(
            fn=validate_and_process,
            inputs=[input_audio],
            outputs=audio_slots + [status_label]
        )

        clear_btn.click(
            fn=clear_all,
            inputs=[],
            outputs=audio_slots + [input_audio, submit_btn, status_label]
        )
            
    return demo