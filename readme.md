# 🎥 Slideshow Pro Maker (GUI V3)

Gerador de vídeos automatizado com interface gráfica, suporte a múltiplas proporções (Instagram, TikTok, YouTube) e mixagem inteligente de áudio.

## ✨ Novidades da V3

* **Seleção de Proporção:** Escolha entre 16:9 (Horizontal), 9:16 (Vertical/Reels), 1:1 (Quadrado) ou 4:3.
* **Sistema de Timestamp:** Os vídeos são salvos com a data e hora no nome (ex: `slideshow_20240520_1530.mp4`), evitando que você perca ou sobrescreva trabalhos anteriores.
* **Verificador de Dependências:** O programa avisa na hora se o `ffmpeg.exe` está faltando e oferece um botão direto para download.
* **Fundo Inteligente Adaptativo:** O efeito de desfoque (Blur) se ajusta automaticamente para preencher qualquer formato de tela escolhido.

## 🚀 Pré-requisitos

### 1. Python e Bibliotecas
Certifique-se de ter o Python 3.x instalado e rode:
```bash
pip install opencv-python numpy
```

### 2. FFmpeg (Essencial para o Áudio)
O programa precisa do motor FFmpeg para colocar a música em loop no vídeo.
* **Download:** [Link direto (Gyan.dev)](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) ou via botão no próprio programa.
* **Instalação:** Extraia o arquivo `.7z`, vá até a pasta `bin`, copie o arquivo **ffmpeg.exe** e cole-o na mesma pasta do script ou do executável final.

## 🛠️ Como criar o Executável (.exe)

Para gerar o binário do Windows e usar o programa sem precisar abrir o código:

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. No terminal, na pasta do projeto, execute:
   ```bash
   python -m PyInstaller --noconsole --onefile gerador_video_gui_v3.py
   ```
3. Pegue o seu `.exe` na pasta `dist/` e coloque o `ffmpeg.exe` junto dele.

## 📦 Formatos Suportados

| Formato | Resolução | Uso Recomendado |
| :--- | :--- | :--- |
| **16:9** | 1920x1080 | YouTube, TV, Apresentações |
| **9:16** | 1080x1920 | TikTok, Instagram Reels, Shorts |
| **1:1** | 1080x1080 | Feed do Instagram, LinkedIn |
| **4:3** | 1440x1080 | Formatos clássicos / iPads |

---
**Nota:** O tempo padrão é de 3 segundos por foto com 1 segundo de transição suave entre elas.