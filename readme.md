# 🎥 Slideshow Pro Maker (V3.1)

Gerador de vídeos profissional com interface gráfica e verificação inteligente de dependências.

## 🚀 Instalação Rápida

1. **Dependências:** `pip install opencv-python numpy`
2. **FFmpeg:** Baixe o `ffmpeg.exe` e coloque na mesma pasta deste script. Se você esquecer, o programa irá te avisar assim que abrir!

## 📂 Organização
* O programa cria automaticamente uma pasta `/output` para salvar seus vídeos.
* Os nomes dos arquivos seguem o padrão: `slideshow_AAAAMMDD_HHMMSS.mp4`.

## 🛠️ Gerar Executável
```bash
python -m PyInstaller --noconsole --onefile gerador_video_gui_v3_1.py
```
*(Lembre-se de copiar o ffmpeg.exe para a pasta do seu novo .exe)*