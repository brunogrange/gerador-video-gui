# 🎥 Slideshow Pro Maker (V3.1)

Professional video generator with a graphical interface and intelligent dependency verification.

## 🚀 Key Features
- **Flexible Aspect Ratios:** Choose from 16:9, 9:16, 1:1, or 4:3 for any social media platform.
- **Adjustable Resolution:** Generate videos in Low-res (480p), HD (720p), Full HD (1080p), or 4K (2160p).
- **Customizable Slide Duration:** Set how long each image stays on screen.
- **Transition Effects:** Select between None, Cross-fade, or Slide (Left/Right) for a polished look.
- **Intelligent Resizing:** Automatically adds a blurred background to maintain your selected aspect ratio without cropping your photos.

## ⚡ Quick Installation

1. **Dependencies:** `pip install opencv-python numpy`
2. **FFmpeg:** Download `ffmpeg.exe` and place it in the same folder as this script. If you forget, the program will warn you as soon as it opens!

## 📂 Organization
* The program automatically creates an `/output` folder to save your videos.
* File names follow the pattern: `slideshow_YYYYMMDD_HHMMSS.mp4`.

## 🛠️ Generate Executable
```bash
python -m PyInstaller --noconsole --onefile gerador_video_gui.py
```
*(Remember to copy `ffmpeg.exe` to your new `.exe` folder)*
