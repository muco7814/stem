import os, time

def process_audio_pipeline(file_path: str) -> dict:
    """
    Mock pipeline contract. Accepts an uploaded track path, 
    simulates processing, and returns paths to output stems.
    """
    print(f"[Pipeline] Starting processing for: {file_path}")
    time.sleep(3) # Simulates Demucs processing time
    
    # Target directory for mock outputs
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)
    
    # Creating empty placeholder files if they don't exist so Gradio doesn't crash
    stems = ["vocals", "kick", "snare", "hats", "instruments"]
    output_paths = {}
    
    for stem in stems:
        path = os.path.join(out_dir, f"mock_{stem}.wav")
        if not os.path.exists(path):
            # Write a tiny blank text/audio placeholder for UI testing
            with open(path, "w") as f:
                f.write("placeholder")
        output_paths[stem] = path
        
    print("[Pipeline] Processing complete.")
    return output_paths