import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import yt_dlp

def escolher_pasta():
    pasta = filedialog.askdirectory()
    caminho_var.set(pasta)

def baixar_video():
    url = entrada_link.get()
    caminho = caminho_var.get()
    resolucao = combo_resolucao.get()
    nome_arquivo = entrada_nome.get()

    if not url or not caminho or not resolucao or not nome_arquivo:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    opcoes = {
        'format': f'bestvideo[height<={resolucao[:-1]}]+bestaudio/best[height<={resolucao[:-1]}]',
        'outtmpl': os.path.join(caminho, f'{nome_arquivo}.%(ext)s')
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        messagebox.showinfo("Sucesso", "Download concluído!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no download:\n{str(e)}")

# Função para centralizar a janela
def centralizar_janela(window, largura, altura):
    largura_tela = window.winfo_screenwidth()
    altura_tela = window.winfo_screenheight()
    x = (largura_tela - largura) // 2
    y = (altura_tela - altura) // 2
    window.geometry(f"{largura}x{altura}+{x}+{y}")

# Janela principal
janela = tk.Tk()
janela.title("Youtube Downloader")
centralizar_janela(janela, 1280, 720)
janela.configure(bg="#f0f0f0")

# Centralizar todos os elementos
frame = tk.Frame(janela, bg="#f0f0f0")
frame.pack(expand=True)

# Link do vídeo
tk.Label(frame, text="Link do vídeo:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=(10, 0))
entrada_link = tk.Entry(frame, width=60)
entrada_link.pack(pady=2)

# Nome do arquivo
tk.Label(frame, text="Nome do arquivo:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=(10, 0))
entrada_nome = tk.Entry(frame, width=60)
entrada_nome.pack(pady=2)

# Caminho para salvar
tk.Label(frame, text="Caminho para salvar:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=(10, 0))
frame_caminho = tk.Frame(frame, bg="#f0f0f0")
frame_caminho.pack(pady=2)
caminho_var = tk.StringVar()
entrada_caminho = tk.Entry(frame_caminho, textvariable=caminho_var, width=50)
entrada_caminho.pack(side=tk.LEFT, padx=5)
botao_pasta = tk.Button(frame_caminho, text="Escolher Pasta", command=escolher_pasta)
botao_pasta.pack(side=tk.LEFT)

# Resolução
tk.Label(frame, text="Resolução:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=(10, 0))
combo_resolucao = ttk.Combobox(frame, values=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"])
combo_resolucao.current(4)
combo_resolucao.pack(pady=2)

# Botões
frame_botoes = tk.Frame(frame, bg="#f0f0f0")
frame_botoes.pack(pady=20)

botao_baixar = tk.Button(frame_botoes, text="Baixar", bg="green", fg="white", width=10, command=baixar_video)
botao_baixar.pack(side=tk.LEFT, padx=10)

botao_sair = tk.Button(frame_botoes, text="Sair", bg="red", fg="white", width=10, command=janela.quit)
botao_sair.pack(side=tk.LEFT, padx=10)

janela.mainloop()
