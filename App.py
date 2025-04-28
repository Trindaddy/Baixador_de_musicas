import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import threading

def baixar_musicas(cantor, quantidade, pasta_destino='.', atualizar_status=None):
    try:
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        pasta_cantor = os.path.join(pasta_destino, cantor)
        os.makedirs(pasta_cantor, exist_ok=True)

        # Caminho para o ffmpeg local (bin/ffmpeg.exe)
        ffmpeg_path = os.path.join(os.getcwd(), 'bin', 'ffmpeg.exe')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(pasta_cantor, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,  # Direto aqui
            'quiet': True,
        }

        ydl = yt_dlp.YoutubeDL(ydl_opts)
        query = f"{cantor} músicas"

        if atualizar_status:
            atualizar_status("Buscando músicas...")

        info = ydl.extract_info(f"ytsearch{quantidade * 2}:{query}", download=False)

        duracao_maxima = 600  # 10 minutos
        musicas_filtradas = []
        for entry in info['entries']:
            if entry['duration'] <= duracao_maxima:
                musicas_filtradas.append(entry)
            if len(musicas_filtradas) >= quantidade:
                break

        if len(musicas_filtradas) == 0:
            messagebox.showwarning("Nenhuma música encontrada", "Não foi possível encontrar músicas com esses critérios.")
            return

        for idx, musica in enumerate(musicas_filtradas, start=1):
            if atualizar_status:
                atualizar_status(f"Baixando ({idx}/{len(musicas_filtradas)}): {musica['title']}")
            ydl.download([musica['webpage_url']])

        if atualizar_status:
            atualizar_status("Download concluído!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entrada_pasta.delete(0, tk.END)
        entrada_pasta.insert(0, pasta)

def iniciar_download_thread():
    t = threading.Thread(target=iniciar_download)
    t.start()

def iniciar_download():
    cantor = entrada_cantor.get()
    quantidade = entrada_quantidade.get()
    pasta_destino = entrada_pasta.get()

    if not cantor or not quantidade:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade precisa ser um número inteiro.")
        return

    if not pasta_destino:
        pasta_destino = '.'

    status_label.config(text="Iniciando download...")
    baixar_musicas(cantor, quantidade, pasta_destino, atualizar_status=lambda msg: status_label.config(text=msg))

# --- Janela principal
janela = tk.Tk()
janela.title("Downloader de Músicas 🎵")
janela.geometry("450x350")
janela.resizable(False, False)

# --- Layout
frame = tk.Frame(janela, padx=20, pady=20)
frame.pack(expand=True)

tk.Label(frame, text="Nome do cantor:", anchor="w").pack(fill='x')
entrada_cantor = tk.Entry(frame)
entrada_cantor.pack(fill='x', pady=5)

tk.Label(frame, text="Quantidade de músicas:", anchor="w").pack(fill='x')
entrada_quantidade = tk.Entry(frame)
entrada_quantidade.pack(fill='x', pady=5)

tk.Label(frame, text="Pasta de destino:", anchor="w").pack(fill='x')
pasta_frame = tk.Frame(frame)
pasta_frame.pack(fill='x', pady=5)

entrada_pasta = tk.Entry(pasta_frame)
entrada_pasta.pack(side=tk.LEFT, expand=True, fill='x')
tk.Button(pasta_frame, text="Selecionar", command=selecionar_pasta, bg="lightblue").pack(side=tk.LEFT, padx=5)

tk.Button(frame, text="Baixar Músicas", command=iniciar_download_thread, bg="green", fg="white", font=('Arial', 12, 'bold')).pack(pady=15)

status_label = tk.Label(janela, text="Aguardando...", relief='sunken', anchor='w')
status_label.pack(fill='x', side='bottom')

# --- Rodar o app
janela.mainloop()
