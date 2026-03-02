# 🎥 Slideshow Pro Maker (V3.1)

Professional video generator with a graphical interface and intelligent dependency verification.

## 🚀 Quick Installation

1. **Dependencies:** `pip install opencv-python numpy`
2. **FFmpeg:** Download `ffmpeg.exe` and place it in the same folder as this script. If you forget, the program will warn you as soon as it opens!

## 📂 Organization
* The program automatically creates an `/output` folder to save your videos.
* File names follow the pattern: `slideshow_YYYYMMDD_HHMMSS.mp4`.

## 🛠️ Generate Executable
```bash
python -m PyInstaller --noconsole --onefile gerador_video_gui.py
```
*(Remember to copy ffmpeg.exe to your new .exe folder)*
