import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def baixar_musicas(cantor, quantidade, duracao_maxima=600, pasta_destino='.'):
    # Cria a pasta de destino, se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Cria uma pasta com o nome do cantor dentro da pasta de destino
    pasta_cantor = os.path.join(pasta_destino, cantor)
    if not os.path.exists(pasta_cantor):
        os.makedirs(pasta_cantor)
    
    # Configurações para o yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(pasta_cantor, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Pesquisar músicas no YouTube
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    query = f"{cantor} músicas"
    
    try:
        info = ydl.extract_info(f"ytsearch{quantidade * 2}:{query}", download=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar músicas: {e}")
        return

    musicas_filtradas = []
    for entry in info['entries']:
        if entry['duration'] <= duracao_maxima:
            musicas_filtradas.append(entry)
        if len(musicas_filtradas) >= quantidade:
            break

    if len(musicas_filtradas) < quantidade:
        messagebox.showinfo("Aviso", f"Encontradas apenas {len(musicas_filtradas)} músicas para o cantor {cantor}.")

    for musica in musicas_filtradas:
        link = musica['webpage_url']
        try:
            ydl.download([link])
        except Exception as e:
            print(f"Erro ao baixar a música {musica['title']}: {e}")

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entrada_pasta.delete(0, tk.END)
        entrada_pasta.insert(0, pasta)

def iniciar_download():
    cantor = entrada_cantor.get()
    quantidade = entrada_quantidade.get()
    duracao_maxima = entrada_duracao.get()
    pasta_destino = entrada_pasta.get()

    if not cantor or not quantidade or not duracao_maxima:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        quantidade = int(quantidade)
        duracao_maxima = int(duracao_maxima)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e duração devem ser números inteiros.")
        return

    minutos = duracao_maxima // 60
    segundos_restantes = duracao_maxima % 60
    messagebox.showinfo("Duração informada", f"{duracao_maxima} segundos equivalem a {minutos} minutos e {segundos_restantes} segundos.")

    if not pasta_destino:
        pasta_destino = '.'

    baixar_musicas(cantor, quantidade, duracao_maxima, pasta_destino)
    messagebox.showinfo("Concluído", "Download das músicas finalizado!")

# Criar janela
janela = tk.Tk()
janela.title("Baixar Músicas do YouTube")
janela.geometry("400x400")
janela.resizable(False, False)

# Rótulos e Entradas
tk.Label(janela, text="Nome do cantor:").pack(pady=5)
entrada_cantor = tk.Entry(janela, width=50)
entrada_cantor.pack()

tk.Label(janela, text="Quantidade de músicas:").pack(pady=5)
entrada_quantidade = tk.Entry(janela, width=50)
entrada_quantidade.pack()

tk.Label(janela, text="Duração máxima (segundos):").pack(pady=5)
entrada_duracao = tk.Entry(janela, width=50)
entrada_duracao.pack()

tk.Label(janela, text="Pasta de destino:").pack(pady=5)
entrada_pasta = tk.Entry(janela, width=40)
entrada_pasta.pack(side=tk.LEFT, padx=(20, 5), pady=10)

botao_selecionar = tk.Button(janela, text="Selecionar", command=selecionar_pasta)
botao_selecionar.pack(side=tk.LEFT)

# Botão para iniciar
tk.Button(janela, text="Baixar Músicas", command=iniciar_download, bg="green", fg="white", font=('Arial', 12, 'bold')).pack(pady=20)

# Rodar o aplicativo
janela.mainloop()
