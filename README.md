# Stem Separation POC

A proof-of-concept repository for audio stem separation and enhancement using Demucs and Gradio.

## What this repo does

- Accepts an uploaded audio mix track via a Gradio web UI
- Uses `demucs` to separate the file into musical stems
- Normalizes the vocal stem with `pydub`
- Returns isolated stems for bass, drums, other, and vocals
- Stores generated stems in `separated_audio/`

## Repository structure

```text
repo/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main entry point that launches the Gradio app
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pipeline.py      # Orchestrates Demucs separation + vocal normalization
│   │   └── enhancer.py      # DSP logic for denoising / spectral repair / exciters
│   └── ui/
│       ├── __init__.py
│       └── interface.py     # Gradio layout and UI control logic
├── outputs/                 # Locally generated stems (ignored by git)
├── separated_audio/         # Runtime output directory for Demucs separation
├── test_files/              # Optional audio files for local testing
├── .gitignore
├── Dockerfile               # Empty placeholder
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10+ recommended
- `pip` package manager
- `ffmpeg` installed on the system for audio handling (required by `pydub` / `demucs`)
- `requirements.txt` contains the required Python packages

### Key Python dependencies

- `gradio`
- `demucs`
- `pydub`
- `torch`
- `torchaudio`
- `librosa`

## Local setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure `ffmpeg` is installed on your machine. For Ubuntu:

```bash
sudo apt update
sudo apt install ffmpeg
```

> If you are on another OS, install `ffmpeg` through your package manager or from https://ffmpeg.org/.

## Run the app

From the repository root:

```bash
python -m app.main
```

Then open the browser at `http://127.0.0.1:7860`.

## Usage

1. Upload a supported audio mix file (`.wav`, `.mp3`, `.flac`, `.aac`, or `.m4a`).
2. Click `Separate & Enhance`.
3. Wait for the pipeline to run. Processing may take several minutes depending on audio length and hardware.
4. Download the isolated stems for bass, drums, other, and vocals.

## Output details

- The pipeline writes separated stems into `separated_audio/`.
- The vocal output is additionally normalized and saved as `*_normalized.wav`.
- The UI exposes four audio download players for:
  - bass
  - drums
  - other
  - vocals

## Notes

- `Dockerfile` is currently empty and not configured for containerized deployment.
- `outputs/` and generated `.wav` files are ignored by git via `.gitignore`.
- The current pipeline uses `demucs.separate` to perform source separation and `pydub` to normalize the vocal stem.

## Reproduction checklist

- `python` version is compatible
- virtual environment active
- `pip install -r requirements.txt` completed successfully
- `ffmpeg` installed
- app started with `python -m app.main`
- browser opened at `http://127.0.0.1:7860`

## Troubleshooting

- If the app fails to launch, check for missing packages or a broken virtual environment.
- If audio separation fails, verify `ffmpeg` is available and the uploaded file is supported.
- If no vocal stem is found, the pipeline will still save the separated stems but may not produce a normalized vocal file.

