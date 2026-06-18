import gradio as gr
import os
from app.core.pipeline import process_audio_pipeline

# Configuration Guards
MAX_FILE_SIZE_MB = 30
ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.m4a']
MAX_STEMS = 10  

def validate_and_process(audio_path):
    if not audio_path:
        return [gr.update(visible=False, value=None) for _ in range(MAX_STEMS)] + [
            gr.update(visible=False)  # status label
        ]
    
    _, ext = os.path.splitext(audio_path.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise gr.Error(f"Unsupported file format. Please upload: {', '.join(ALLOWED_EXTENSIONS)}")
        
    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise gr.Error(f"File size exceeds maximum limit of {MAX_FILE_SIZE_MB}MB. (Your file: {file_size_mb:.2f}MB)")

    stems = process_audio_pipeline(audio_path)
    
    ui_updates = []
    stem_items = list(stems.items())
    
    for i in range(MAX_STEMS):
        if i < len(stem_items):
            stem_name, file_path = stem_items[i]
            ui_updates.append(gr.update(
                visible=True, 
                label=f"Isolated Component: {stem_name.upper()}", 
                value=file_path
            ))
        else:
            ui_updates.append(gr.update(visible=False, value=None))
    
    # Hide loading indicators on completion
    ui_updates.append(gr.update(visible=False))  # status label
            
    return ui_updates

def clear_all():
    updates = [gr.update(visible=False, value=None) for _ in range(MAX_STEMS)]
    updates.append(gr.update(value=None))        # input audio
    updates.append(gr.update(interactive=False)) # submit button
    updates.append(gr.update(visible=False))     # status label
    return updates

def show_loading():
    """Show loading indicators when processing starts"""
    updates = [gr.update(visible=False, value=None) for _ in range(MAX_STEMS)]
    updates.append(gr.update(visible=True, value="⏳ Processing... This may take a few minutes."))  # status
    return updates

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
                
                # Progress Bar
                progress_bar = gr.Progress(track_tqdm=True)

            # SPACER INTERSTICE (Visual Padding Division)
            with gr.Column(scale=1):
                gr.Markdown(" ")

            # RIGHT COLUMN (Larger footprint: Performance Stem Arrays)
            with gr.Column(scale=4):
                gr.Markdown("### 🔊 Enhanced Stem Multi-Tracks")
                
                audio_slots = []
                for i in range(MAX_STEMS):
                    slot = gr.Audio(
                        label=f"Stem Slot {i+1}", 
                        type="filepath",
                        interactive=False,
                        visible=False  
                    )
                    audio_slots.append(slot)

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