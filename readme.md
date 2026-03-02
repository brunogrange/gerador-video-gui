# 🎥 Slideshow Pro Maker (GUI)

Este é um gerador de vídeos de slideshow automatizado com interface gráfica (GUI), desenvolvido em Python. Ele transforma suas fotos em um vídeo dinâmico com transições suaves, música de fundo e uma imagem de destaque recorrente.

## ✨ Funcionalidades

* **Interface Gráfica (Tkinter):** Escolha arquivos e pastas visualmente, sem mexer no código.
* **Imagem de Destaque:** Define uma imagem específica (ex: sua logo ou marca) para aparecer a cada 20 fotos.
* **Seleção Múltipla:** Adicione centenas de imagens de uma só vez via seletor de arquivos.
* **Fundo Inteligente:** Aplica preenchimento com desfoque (Blur) para fotos que não estão na proporção 16:9, eliminando as barras pretas.
* **Áudio em Loop:** A música escolhida é repetida automaticamente até o final do vídeo usando FFmpeg.
* **Transições Suaves:** Efeito de cross-fade (dissolvência) entre os slides.

## 🚀 Pré-requisitos

### 1. Python e Bibliotecas
Tenha o Python 3.x instalado e instale as dependências necessárias:
```bash
pip install opencv-python numpy
```

### 2. FFmpeg (Obrigatório para o Áudio)
O script utiliza o FFmpeg para realizar a mixagem de áudio e vídeo.
* **Onde baixar:** * Site oficial: [ffmpeg.org](https://ffmpeg.org/download.html)
    * Link direto para Windows (Recomendado): [Gyan.dev (ffmpeg-git-essentials.7z)](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z)
* **Instalação rápida:** 1. Baixe e extraia o arquivo.
    2. Entre na pasta `bin`.
    3. Copie o arquivo **ffmpeg.exe**.
    4. Cole-o **na mesma pasta** onde está o seu script `.py` (ou o seu arquivo `.exe` gerado).

## 🛠️ Gerando o Executável (.exe) no Windows

Para criar um binário que rode em qualquer computador sem precisar instalar o Python:

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. No terminal, dentro da pasta do projeto, execute:
   ```bash
   pyinstaller --noconsole --onefile gerador_video_gui.py
   ```
3. O arquivo `.exe` será gerado dentro da pasta `dist/`. 
   * **Importante:** O arquivo `ffmpeg.exe` deve estar na mesma pasta do executável para que a música funcione.

## 📦 Tecnologias Utilizadas

* **Python**
* **OpenCV**: Renderização de imagem e vídeo.
* **Tkinter**: Interface gráfica nativa.
* **FFmpeg**: Motor de processamento de áudio.
* **Numpy**: Processamento de matrizes de imagem.

---
Desenvolvido para automatizar a criação de conteúdo visual de forma rápida e prática.