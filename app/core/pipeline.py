import os
import shutil
from demucs import separate
from pydub import AudioSegment
from pydub.silence import split_on_silence

def process_audio_pipeline(file_path: str) -> dict:
    """
    Processes audio file using Demucs to separate tracks into stems,
    then normalizes the vocal track and returns the normalized audio file.
    """
    print(f"[Pipeline] Starting processing for: {file_path}")
    
    # Define the output directory for the separated tracks
    output_dir = './separated_audio'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Separating tracks for {file_path}...")
    
    # Use demucs to separate the audio tracks
    separate.main([file_path, '-o', output_dir])
    
    print("Separation complete. Check the 'separated_audio' directory for results.")
    
    # List the generated files
    separated_files = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            separated_files.append(os.path.join(root, file))
    
    print("\nGenerated files:")
    for f in separated_files:
        print(f)
    
    # Find and normalize the vocal track
    vocals_path = None
    for file_path_item in separated_files:
        if 'vocals' in file_path_item.lower() and file_path_item.endswith('.wav'):
            vocals_path = file_path_item
            break
    
    output_paths = {}
    
    if vocals_path:
        print(f"\nNormalizing vocal track: {vocals_path}")
        
        # Load the vocal track
        vocal_audio = AudioSegment.from_wav(vocals_path)
        
        # Normalize the audio to -20 dBFS (decibels relative to full scale)
        normalized_vocal_audio = vocal_audio.normalize(headroom=0.0)
        
        # Export the normalized audio
        normalized_vocals_path = vocals_path.replace('.wav', '_normalized.wav')
        normalized_vocal_audio.export(normalized_vocals_path, format="wav")
        
        print(f"Normalized vocal track saved to: {normalized_vocals_path}")
        
        # Return the normalized file as the final output
        output_paths['vocal_normalized'] = normalized_vocals_path
    else:
        print("Warning: No vocal track found in separated files.")
    
    # Also return all separated files for reference
    for i, file_path_item in enumerate(separated_files):
        output_paths[f"stem_{i}"] = file_path_item
    
    print("[Pipeline] Processing complete.")
    return output_paths