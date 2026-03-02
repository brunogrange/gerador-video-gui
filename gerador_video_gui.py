import cv2
import os
import numpy as np
import random
import subprocess 
import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import webbrowser
from datetime import datetime

class VideoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slideshow Pro Maker - V3.1")
        self.root.geometry("600x750")
        
        self.main_path = tk.StringVar()
        self.audio_path = tk.StringVar()
        self.selected_ratio = tk.StringVar(value="16:9 (YouTube)")
        self.slide_duration = tk.IntVar(value=10)
        self.transition_effect = tk.StringVar(value="Cross-fade")
        self.photo_list = []
        
        self.formats = {
            "16:9 (YouTube)": (1920, 1080),
            "9:16 (TikTok/Reels)": (1080, 1920),
            "1:1 (Instagram Post)": (1080, 1080),
            "4:3 (Old/TV)": (1440, 1080)
        }

        self.effects = ["None", "Cross-fade", "Slide (Left/Right)"]
        
        self.setup_ui()
        
        # STARTUP CHECK
        self.root.after(500, self.check_ffmpeg_startup)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- FFmpeg Alert Frame (Top) ---
        self.alert_frame = ttk.Frame(main_frame)
        self.lbl_ffmpeg_status = ttk.Label(self.alert_frame, text="", font=('Segoe UI', 9, 'bold'))
        self.lbl_ffmpeg_status.pack(side=tk.LEFT)
        self.btn_download_ffmpeg = ttk.Button(self.alert_frame, text="Download FFmpeg", command=self.open_ffmpeg_download)
        self.alert_frame.pack(fill=tk.X, pady=(0, 10))

        # --- Ratio Selection ---
        ttk.Label(main_frame, text="Video Aspect Ratio:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.combo_ratio = ttk.Combobox(main_frame, textvariable=self.selected_ratio, values=list(self.formats.keys()), state="readonly")
        self.combo_ratio.pack(fill=tk.X, pady=5)

        # --- Slide Settings ---
        f_config = ttk.Frame(main_frame)
        f_config.pack(fill=tk.X, pady=10)
        
        f_duration = ttk.Frame(f_config)
        f_duration.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(f_duration, text="Duration (sec):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        ttk.Spinbox(f_duration, from_=1, to=60, textvariable=self.slide_duration).pack(fill=tk.X, padx=(0, 5))

        f_effect = ttk.Frame(f_config)
        f_effect.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(f_effect, text="Transition:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        ttk.Combobox(f_effect, textvariable=self.transition_effect, values=self.effects, state="readonly").pack(fill=tk.X)

        # --- File Selection ---
        ttk.Label(main_frame, text="Featured Image (Repeats every 20):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        f_main = ttk.Frame(main_frame); f_main.pack(fill=tk.X)
        ttk.Entry(f_main, textvariable=self.main_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_main, text="Browse", command=self.select_main).pack(side=tk.RIGHT)

        ttk.Label(main_frame, text="Background Music (.mp3):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        f_audio = ttk.Frame(main_frame); f_audio.pack(fill=tk.X)
        ttk.Entry(f_audio, textvariable=self.audio_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_audio, text="Browse", command=self.select_audio).pack(side=tk.RIGHT)

        ttk.Label(main_frame, text="Slideshow Photos:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        ttk.Button(main_frame, text="Select Multiple Photos", command=self.select_photos).pack(fill=tk.X)
        self.lbl_count = ttk.Label(main_frame, text="No photos selected."); self.lbl_count.pack(anchor=tk.W)

        # --- Progress ---
        self.progress = ttk.Progressbar(main_frame, mode='determinate'); self.progress.pack(fill=tk.X, pady=20)
        self.lbl_status = ttk.Label(main_frame, text="Waiting...", foreground="gray"); self.lbl_status.pack()

        # --- Generate Button ---
        self.btn_generate = ttk.Button(main_frame, text="GENERATE VIDEO", command=self.start_thread)
        self.btn_generate.pack(side=tk.BOTTOM, pady=20, fill=tk.X)

    def check_ffmpeg_startup(self):
        """Checks for FFmpeg on startup"""
        if not os.path.exists("ffmpeg.exe"):
            self.lbl_ffmpeg_status.config(text="✘ FFmpeg NOT FOUND!", foreground="red")
            self.btn_download_ffmpeg.pack(side=tk.RIGHT, padx=5)
            messagebox.showwarning("Dependency Warning", 
                "'ffmpeg.exe' was not found in the folder.\n\n"
                "You can still generate the video, but it will have NO AUDIO.\n"
                "Click 'Download FFmpeg' to fix this.")
        else:
            self.lbl_ffmpeg_status.config(text="✔ FFmpeg detected!", foreground="green")
            self.btn_download_ffmpeg.pack_forget()

    def open_ffmpeg_download(self):
        webbrowser.open("https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z")

    def select_main(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path: self.main_path.set(path)

    def select_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3")])
        if path: self.audio_path.set(path)

    def select_photos(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if paths:
            self.photo_list = list(paths)
            self.lbl_count.config(text=f"{len(self.photo_list)} photos selected.")

    def prepare_image(self, path, width, height):
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None: return None
        h, w = img.shape[:2]
        esc_f = max(width/w, height/h)
        bg = cv2.resize(img, (math.ceil(w * esc_f), math.ceil(h * esc_f)))
        y_c, x_c = (bg.shape[0]-height)//2, (bg.shape[1]-width)//2
        bg = cv2.GaussianBlur(bg[y_c:y_c+height, x_c:x_c+width], (101, 101), 0)
        esc_v = min(width/w, height/h)
        fg = cv2.resize(img, (int(w*esc_v), int(h*esc_v)))
        yf, xf = (height-fg.shape[0])//2, (width-fg.shape[1])//2
        bg[yf:yf+fg.shape[0], xf:xf+fg.shape[1]] = fg
        return bg

    def start_thread(self):
        if not self.photo_list: return messagebox.showwarning("Error", "Select photos first!")
        self.btn_generate.config(state=tk.DISABLED)
        threading.Thread(target=self.process_video, daemon=True).start()

    def process_video(self):
        try:
            # Create output folder if it doesn't exist
            if not os.path.exists("output"): os.makedirs("output")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            width, height = self.formats[self.selected_ratio.get()]
            temp_name = f"output/temp_{timestamp}.mp4"
            final_name = f"output/slideshow_{timestamp}.mp4"

            sequence = []
            photos = self.photo_list.copy()
            random.shuffle(photos)
            main_img = self.main_path.get()
            for i, f in enumerate(photos):
                if main_img and i % 20 == 0: sequence.append(main_img)
                sequence.append(f)

            self.progress["maximum"] = len(sequence)
            video = cv2.VideoWriter(temp_name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
            
            fps = 30
            transition_frames = 30 # 1 second
            static_frames = (self.slide_duration.get() * fps) - transition_frames
            if static_frames < 0: static_frames = 0

            effect = self.transition_effect.get()
            
            prev_img = None
            for i, path in enumerate(sequence):
                self.lbl_status.config(text=f"Processing {i+1}/{len(sequence)}...")
                self.progress["value"] = i + 1
                curr_img = self.prepare_image(path, width, height)
                if curr_img is None: continue

                # Transition
                if prev_img is not None:
                    if effect == "Cross-fade":
                        for j in range(transition_frames):
                            a = j/transition_frames
                            video.write(cv2.addWeighted(prev_img, 1-a, curr_img, a, 0))
                    elif effect == "Slide (Left/Right)":
                        for j in range(transition_frames):
                            offset = int((j/transition_frames) * width)
                            frame = np.zeros((height, width, 3), dtype=np.uint8)
                            frame[:, :width-offset] = prev_img[:, offset:]
                            frame[:, width-offset:] = curr_img[:, :offset]
                            video.write(frame)
                    # "None" does nothing here
                
                # Static frames for current slide
                for _ in range(static_frames):
                    video.write(curr_img)
                
                prev_img = curr_img
            
            video.release()

            audio = self.audio_path.get()
            if audio and os.path.exists("ffmpeg.exe"):
                self.lbl_status.config(text="Mixing audio...")
                cmd = ["ffmpeg.exe", "-y", "-i", temp_name, "-stream_loop", "-1", "-i", audio, 
                       "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest", final_name]
                subprocess.run(cmd, check=True, creationflags=0x08000000)
                if os.path.exists(temp_name): os.remove(temp_name)
                res = final_name
            else:
                res = temp_name

            messagebox.showinfo("Success", f"Video saved in output folder:\n{os.path.basename(res)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.lbl_status.config(text="Ready!")
            self.btn_generate.config(state=tk.NORMAL)
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGeneratorApp(root)
    root.mainloop()
