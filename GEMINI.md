# 🎥 Slideshow Pro Maker (V3.1) - Project Context

This project is a Python desktop tool for automated slideshow video creation, featuring smooth transitions and soundtrack support.

## 🚀 Project Overview
- **Goal:** Simplify the creation of videos for social media (TikTok, Reels, YouTube) from a collection of photos.
- **Interface:** Built with **Tkinter**, providing a visual experience for file selection and parameter configuration.
- **Processing:** Uses **OpenCV** for video rendering and **NumPy** for image matrix manipulation.
- **Audio:** Relies on the external **FFmpeg** binary to perform muxing (merging) the video with MP3 audio.

## 🛠️ Technologies and Dependencies
- **Language:** Python 3.x
- **Python Libraries:**
  - `opencv-python`: Image processing and video writing.
  - `numpy`: Mathematical support for pixel manipulation.
  - `tkinter`: Standard Python GUI.
- **External Dependency:** `ffmpeg.exe` (must be in the root directory for audio support).

## 🏃 How to Run the Project

### Prerequisites
1. Install dependencies:
   ```bash
   pip install opencv-python numpy
   ```
2. Ensure `ffmpeg.exe` is in the root folder.

### Execution
To start the graphical interface:
```bash
python gerador_video_gui.py
```

### Generate Executable (Windows)
The project uses PyInstaller to generate a single `.exe` file:
```bash
python -m PyInstaller --noconsole --onefile gerador_video_gui.py
```
*Note: After generating the executable, `ffmpeg.exe` must be kept in the same folder as the generated file.*

## 📂 Structure and Conventions
- **Input:** Accepts images (.jpg, .jpeg, .png) and audio (.mp3).
- **Output:** Videos are automatically saved in the `/output` folder with the naming pattern `slideshow_YYYYMMDD_HHMMSS.mp4`.
- **Architecture:**
  - Video processing occurs in a separate `threading.Thread` to prevent the interface (GUI) from freezing.
  - The `prepare_image` method handles intelligent resizing, creating a blurred background to maintain the selected aspect ratio.
  - Supported formats: 16:9, 9:16, 1:1, and 4:3.

## 📝 Development Notes
- When modifying `gerador_video_gui.py`, ensure compatibility with the FFmpeg binary.
- FFmpeg existence check occurs at application startup (`check_ffmpeg_startup`).
- Transition effects include "None", "Cross-fade", and "Slide (Left/Right)".
- Slide duration is configurable, with a 1-second (30 frames) transition period.
