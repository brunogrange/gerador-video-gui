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
        self.root.title("Criador de Slideshow Pro - V3.1")
        self.root.geometry("600x650")
        
        self.caminho_main = tk.StringVar()
        self.caminho_audio = tk.StringVar()
        self.proporcao_selecionada = tk.StringVar(value="16:9 (YouTube)")
        self.lista_fotos = []
        
        self.formatos = {
            "16:9 (YouTube)": (1920, 1080),
            "9:16 (TikTok/Reels)": (1080, 1920),
            "1:1 (Instagram Post)": (1080, 1080),
            "4:3 (Antigo/TV)": (1440, 1080)
        }
        
        self.setup_ui()
        
        # VERIFICAÇÃO NO STARTUP
        self.root.after(500, self.alerta_startup_ffmpeg)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Frame de Alerta FFmpeg (Fica no topo) ---
        self.frame_alerta = ttk.Frame(main_frame)
        self.lbl_ffmpeg_status = ttk.Label(self.frame_alerta, text="", font=('Segoe UI', 9, 'bold'))
        self.lbl_ffmpeg_status.pack(side=tk.LEFT)
        self.btn_baixar_ffmpeg = ttk.Button(self.frame_alerta, text="Baixar FFmpeg", command=self.abrir_download_ffmpeg)
        self.frame_alerta.pack(fill=tk.X, pady=(0, 10))

        # --- Seleção de Proporção ---
        ttk.Label(main_frame, text="Proporção do Vídeo:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.combo_proporcao = ttk.Combobox(main_frame, textvariable=self.proporcao_selecionada, values=list(self.formatos.keys()), state="readonly")
        self.combo_proporcao.pack(fill=tk.X, pady=5)

        # --- Seleção de Arquivos ---
        ttk.Label(main_frame, text="Imagem de Destaque (Repete a cada 20):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        f_main = ttk.Frame(main_frame); f_main.pack(fill=tk.X)
        ttk.Entry(f_main, textvariable=self.caminho_main).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_main, text="Buscar", command=self.selecionar_main).pack(side=tk.RIGHT)

        ttk.Label(main_frame, text="Música de Fundo (.mp3):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        f_audio = ttk.Frame(main_frame); f_audio.pack(fill=tk.X)
        ttk.Entry(f_audio, textvariable=self.caminho_audio).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_audio, text="Buscar", command=self.selecionar_audio).pack(side=tk.RIGHT)

        ttk.Label(main_frame, text="Fotos do Slideshow:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        ttk.Button(main_frame, text="Selecionar Múltiplas Fotos", command=self.selecionar_fotos).pack(fill=tk.X)
        self.lbl_contagem = ttk.Label(main_frame, text="Nenhuma foto selecionada."); self.lbl_contagem.pack(anchor=tk.W)

        # --- Progresso ---
        self.progresso = ttk.Progressbar(main_frame, mode='determinate'); self.progresso.pack(fill=tk.X, pady=20)
        self.lbl_status = ttk.Label(main_frame, text="Aguardando...", foreground="gray"); self.lbl_status.pack()

        # --- Botão Gerar ---
        self.btn_gerar = ttk.Button(main_frame, text="GERAR VÍDEO", command=self.iniciar_thread)
        self.btn_gerar.pack(side=tk.BOTTOM, pady=20, fill=tk.X)

    def alerta_startup_ffmpeg(self):
        """Verifica o FFmpeg assim que o programa abre"""
        if not os.path.exists("ffmpeg.exe"):
            self.lbl_ffmpeg_status.config(text="✘ FFmpeg NÃO ENCONTRADO!", foreground="red")
            self.btn_baixar_ffmpeg.pack(side=tk.RIGHT, padx=5)
            messagebox.showwarning("Aviso de Dependência", 
                "O arquivo 'ffmpeg.exe' não foi encontrado na pasta.\n\n"
                "Você poderá gerar o vídeo, mas ele ficará SEM ÁUDIO.\n"
                "Clique no botão 'Baixar FFmpeg' para resolver.")
        else:
            self.lbl_ffmpeg_status.config(text="✔ FFmpeg detectado!", foreground="green")
            self.btn_baixar_ffmpeg.pack_forget()

    def abrir_download_ffmpeg(self):
        webbrowser.open("https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z")

    def selecionar_main(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if path: self.caminho_main.set(path)

    def selecionar_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Áudio", "*.mp3")])
        if path: self.caminho_audio.set(path)

    def selecionar_fotos(self):
        paths = filedialog.askopenfilenames(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if paths:
            self.lista_fotos = list(paths)
            self.lbl_contagem.config(text=f"{len(self.lista_fotos)} fotos selecionadas.")

    def preparar_imagem(self, caminho, largura, altura):
        img = cv2.imdecode(np.fromfile(caminho, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None: return None
        h, w = img.shape[:2]
        esc_f = max(largura/w, altura/h)
        fundo = cv2.resize(img, (math.ceil(w * esc_f), math.ceil(h * esc_f)))
        y_c, x_c = (fundo.shape[0]-altura)//2, (fundo.shape[1]-largura)//2
        fundo = cv2.GaussianBlur(fundo[y_c:y_c+altura, x_c:x_c+largura], (101, 101), 0)
        esc_v = min(largura/w, altura/h)
        frente = cv2.resize(img, (int(w*esc_v), int(h*esc_v)))
        yf, xf = (altura-frente.shape[0])//2, (largura-frente.shape[1])//2
        fundo[yf:yf+frente.shape[0], xf:xf+frente.shape[1]] = frente
        return fundo

    def iniciar_thread(self):
        if not self.lista_fotos: return messagebox.showwarning("Erro", "Selecione as fotos!")
        self.btn_gerar.config(state=tk.DISABLED)
        threading.Thread(target=self.processar_video, daemon=True).start()

    def processar_video(self):
        try:
            # Criar pasta de saída se não existir
            if not os.path.exists("output"): os.makedirs("output")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            largura, altura = self.formatos[self.proporcao_selecionada.get()]
            nome_temp = f"output/temp_{timestamp}.mp4"
            nome_final = f"output/slideshow_{timestamp}.mp4"

            sequencia = []
            fotos = self.lista_fotos.copy()
            random.shuffle(fotos)
            main_img = self.caminho_main.get()
            for i, f in enumerate(fotos):
                if main_img and i % 20 == 0: sequencia.append(main_img)
                sequencia.append(f)

            self.progresso["maximum"] = len(sequencia)
            video = cv2.VideoWriter(nome_temp, cv2.VideoWriter_fourcc(*'mp4v'), 30, (largura, altura))
            
            img_ant = None
            for i, cam in enumerate(sequencia):
                self.lbl_status.config(text=f"Processando {i+1}/{len(sequencia)}...")
                self.progresso["value"] = i + 1
                img_at = self.preparar_imagem(cam, largura, altura)
                if img_at is None: continue
                if img_ant is not None:
                    for j in range(30):
                        a = j/30
                        video.write(cv2.addWeighted(img_ant, 1-a, img_at, a, 0))
                for _ in range(90): video.write(img_at)
                img_ant = img_at
            video.release()

            audio = self.caminho_audio.get()
            if audio and os.path.exists("ffmpeg.exe"):
                self.lbl_status.config(text="Mixando áudio...")
                cmd = ["ffmpeg.exe", "-y", "-i", nome_temp, "-stream_loop", "-1", "-i", audio, 
                       "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest", nome_final]
                subprocess.run(cmd, check=True, creationflags=0x08000000)
                if os.path.exists(nome_temp): os.remove(nome_temp)
                res = nome_final
            else:
                res = nome_temp

            messagebox.showinfo("Sucesso", f"Vídeo salvo na pasta output:\n{os.path.basename(res)}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.lbl_status.config(text="Pronto!")
            self.btn_gerar.config(state=tk.NORMAL)
            self.progresso["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGeneratorApp(root)
    root.mainloop()