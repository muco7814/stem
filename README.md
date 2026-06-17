# Stem Separation POC

## Directory Strucutre: 

```text
repo/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main entry point that boots the Gradio app
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pipeline.py      # Orchestrates Demucs -> Drum Split -> Enhancer
│   │   └── enhancer.py      # DSP logic (Denoising, Spectral Repair, Exciters)
│   └── ui/
│       ├── __init__.py
│       └── interface.py     # Contains the Gradio layout and UI logic
├── outputs/                 # Locally generated stems go here (added in gitignore)
├── test_files/              # Store File A and File B here for quick testing
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt


