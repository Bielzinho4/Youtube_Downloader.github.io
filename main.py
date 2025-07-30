import tkinter as tk
from tkinter import filedialog, messagebox
import os
from yt_dlp import YoutubeDL

def escolher_diretorio():
    pasta = filedialog.askdirectory()
    if pasta:
        entrada_caminho.delete(0, tk.END)
        entrada_caminho.insert(0, pasta)

def baixar_video():
    url = entrada_url.get().strip()
    qualidade = qualidade_var.get()
    nome_arquivo = entrada_nome.get().strip()
    caminho = entrada_caminho.get().strip()

    if not url or not nome_arquivo or not caminho:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    extensao = ""
    ydl_opts = {}

    if qualidade == "MP3 (áudio)":
        extensao = "mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(caminho, nome_arquivo + '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
    elif qualidade == "MP4 480p":
        extensao = "mp4"
        ydl_opts = {
            'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
            'outtmpl': os.path.join(caminho, nome_arquivo + '.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
        }
    elif qualidade == "MP4 720p":
        extensao = "mp4"
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best',
            'outtmpl': os.path.join(caminho, nome_arquivo + '.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
        }
    elif qualidade == "MP4 1080p":
        extensao = "mp4"
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': os.path.join(caminho, nome_arquivo + '.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
        }
    elif qualidade == "GIF":
        extensao = "gif"
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(caminho, nome_arquivo + '.mp4'),
            'quiet': True,
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if qualidade == "GIF":
            converter_para_gif(os.path.join(caminho, nome_arquivo + ".mp4"), os.path.join(caminho, nome_arquivo + ".gif"))
        messagebox.showinfo("Sucesso", f"Download concluído como {nome_arquivo}.{extensao}")
    except Exception as e:
        messagebox.showerror("Erro no download", str(e))

def converter_para_gif(input_path, output_path):
    import subprocess
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-vf", "fps=10,scale=320:-1:flags=lanczos",
            "-loop", "0", output_path
        ])
        os.remove(input_path)
    except Exception as e:
        messagebox.showerror("Erro ao converter para GIF", str(e))

janela = tk.Tk()
janela.title("Downloader de Vídeos")
janela.geometry("500x420")

tk.Label(janela, text="URL do vídeo:", font=("Arial", 12)).pack(pady=5)
entrada_url = tk.Entry(janela, width=60)
entrada_url.pack(pady=5)

tk.Label(janela, text="Qualidade:", font=("Arial", 12)).pack(pady=5)
opcoes_qualidade = ["MP3 (áudio)", "MP4 480p", "MP4 720p", "MP4 1080p", "GIF"]
qualidade_var = tk.StringVar()
qualidade_var.set(opcoes_qualidade[0])
menu_qualidade = tk.OptionMenu(janela, qualidade_var, *opcoes_qualidade)
menu_qualidade.pack(pady=5)

tk.Label(janela, text="Nome do arquivo:", font=("Arial", 12)).pack(pady=5)
entrada_nome = tk.Entry(janela, width=60)
entrada_nome.pack(pady=5)

tk.Label(janela, text="Caminho para salvar:", font=("Arial", 12)).pack(pady=5)
entrada_caminho = tk.Entry(janela, width=45)
entrada_caminho.pack(side=tk.LEFT, padx=(20,0), pady=5)
botao_escolher = tk.Button(janela, text="Escolher", command=escolher_diretorio)
botao_escolher.pack(side=tk.LEFT, padx=10, pady=5)

botao_baixar = tk.Button(janela, text="Baixar", font=("Arial", 12), bg="green", fg="white", command=baixar_video)
botao_baixar.pack(pady=20)

janela.mainloop()
