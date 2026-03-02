import cv2
import os
import numpy as np
import random
import subprocess 
import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class VideoGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criador de Slideshow Pro")
        self.root.geometry("600x500")
        
        # Variáveis de dados
        self.caminho_main = tk.StringVar()
        self.caminho_audio = tk.StringVar()
        self.lista_fotos = []
        
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TButton", padding=5)
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Seleção de Imagem de Destaque ---
        ttk.Label(main_frame, text="Imagem de Destaque (Repete a cada 20 fotos):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        f_main = ttk.Frame(main_frame)
        f_main.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(f_main, textvariable=self.caminho_main).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_main, text="Selecionar", command=self.selecionar_main).pack(side=tk.RIGHT)

        # --- Seleção de Áudio ---
        ttk.Label(main_frame, text="Música de Fundo (.mp3):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        f_audio = ttk.Frame(main_frame)
        f_audio.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(f_audio, textvariable=self.caminho_audio).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_audio, text="Selecionar", command=self.selecionar_audio).pack(side=tk.RIGHT)

        # --- Seleção de Múltiplas Fotos ---
        ttk.Label(main_frame, text="Fotos do Slideshow:", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        self.btn_fotos = ttk.Button(main_frame, text="Selecionar Múltiplas Fotos", command=self.selecionar_fotos)
        self.btn_fotos.pack(fill=tk.X, pady=(0, 5))
        
        self.lbl_contagem = ttk.Label(main_frame, text="Nenhuma foto selecionada.")
        self.lbl_contagem.pack(anchor=tk.W)

        # --- Progresso e Status ---
        self.progresso = ttk.Progressbar(main_frame, mode='determinate')
        self.progresso.pack(fill=tk.X, pady=20)
        
        self.lbl_status = ttk.Label(main_frame, text="Aguardando início...", foreground="gray")
        self.lbl_status.pack()

        # --- Botão Gerar ---
        self.btn_gerar = ttk.Button(main_frame, text="GERAR VÍDEO FINAL", command=self.iniciar_thread)
        self.btn_gerar.pack(side=tk.BOTTOM, pady=20, fill=tk.X)

    # --- Funções de Seleção ---
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

    # --- Lógica de Processamento (Igual à sua, adaptada) ---
    def preparar_imagem(self, caminho, largura=1920, altura=1080):
        img = cv2.imdecode(np.fromfile(caminho, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None: return None
        h, w = img.shape[:2]
        
        escala_fundo = max(largura/w, altura/h)
        w_fundo = max(largura, math.ceil(w * escala_fundo))
        h_fundo = max(altura, math.ceil(h * escala_fundo))
        fundo = cv2.resize(img, (w_fundo, h_fundo))
        y_c = max(0, (h_fundo - altura) // 2)
        x_c = max(0, (w_fundo - largura) // 2)
        fundo = fundo[y_c:y_c+altura, x_c:x_c+largura]
        fundo = cv2.GaussianBlur(fundo, (101, 101), 0)
        
        escala_frente = min(largura/w, altura/h)
        novo_w = min(largura, int(w * escala_frente))
        novo_h = min(altura, int(h * escala_frente))
        img_frente = cv2.resize(img, (novo_w, novo_h))
        x_offset = max(0, (largura - novo_w) // 2)
        y_offset = max(0, (altura - novo_h) // 2)
        fundo[y_offset:y_offset+novo_h, x_offset:x_offset+novo_w] = img_frente
        return fundo

    def iniciar_thread(self):
        if not self.lista_fotos:
            messagebox.showwarning("Erro", "Selecione pelo menos algumas fotos!")
            return
        self.btn_gerar.config(state=tk.DISABLED)
        threading.Thread(target=self.processar_video, daemon=True).start()

    def processar_video(self):
        try:
            largura, altura = 1920, 1080
            fps = 30
            tempo_foto = 3
            tempo_transicao = 1
            nome_video_temp = "temp_video_mudo.mp4"
            nome_video_final = "slideshow_FINAL.mp4"

            # Organiza sequência
            fotos_sorteadas = self.lista_fotos.copy()
            random.shuffle(fotos_sorteadas)
            
            sequencia = []
            main_path = self.caminho_main.get()
            for i, foto in enumerate(fotos_sorteadas):
                if main_path and i % 20 == 0:
                    sequencia.append(main_path)
                sequencia.append(foto)

            self.progresso["maximum"] = len(sequencia)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(nome_video_temp, fourcc, fps, (largura, altura))
            
            img_anterior = None
            for i, caminho in enumerate(sequencia):
                self.lbl_status.config(text=f"Processando foto {i+1} de {len(sequencia)}...")
                self.progresso["value"] = i + 1
                
                img_atual = self.preparar_imagem(caminho)
                if img_atual is None: continue
                
                if img_anterior is not None:
                    for j in range(fps * tempo_transicao):
                        alpha = j / (fps * tempo_transicao)
                        frame = cv2.addWeighted(img_anterior, 1 - alpha, img_atual, alpha, 0)
                        video.write(frame)
                
                for _ in range(fps * tempo_foto):
                    video.write(img_atual)
                img_anterior = img_atual
            
            video.release()

            # Mixagem de Áudio
            audio_path = self.caminho_audio.get()
            if audio_path and os.path.exists("ffmpeg.exe"):
                self.lbl_status.config(text="Adicionando áudio com FFmpeg...")
                comando = [
                    "ffmpeg.exe", "-y", "-i", nome_video_temp,
                    "-stream_loop", "-1", "-i", audio_path,
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-shortest", nome_video_final
                ]
                subprocess.run(comando, check=True, creationflags=0x08000000) # Esconde janela cmd
                if os.path.exists(nome_video_temp): os.remove(nome_video_temp)
                res_path = nome_video_final
            else:
                res_path = nome_video_temp

            messagebox.showinfo("Sucesso", f"Vídeo gerado: {res_path}")
        except Exception as e:
            messagebox.showerror("Erro Crítico", str(e))
        finally:
            self.lbl_status.config(text="Pronto!")
            self.btn_gerar.config(state=tk.NORMAL)
            self.progresso["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGeneratorApp(root)
    root.mainloop()