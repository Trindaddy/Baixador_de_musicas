# Downloader de Músicas do YouTube

Este projeto permite baixar músicas do YouTube em formato MP3 de um cantor ou banda específica, com opções de duração máxima e quantidade de músicas. A aplicação também permite salvar as músicas em uma pasta de destino personalizada.

## Funcionalidades

- Pesquise e baixe músicas de um cantor específico no YouTube.
- Selecione a quantidade de músicas que deseja baixar.
- Defina a duração máxima das músicas.
- Escolha a pasta onde as músicas serão salvas.
- As músicas serão baixadas em formato MP3, com qualidade de 192 kbps.

## Requisitos

- Python 3.x
- yt-dlp
- FFmpeg

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/seuusuario/downloader-musicas-youtube.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd downloader-musicas-youtube
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Como usar

1. Execute o script principal `baixar_musicas.py`:
    ```bash
    python baixar_musicas.py
    ```

2. Siga as instruções para inserir o nome do cantor, a quantidade de músicas e a duração máxima. Também será possível definir a pasta de destino para os arquivos baixados.

3. As músicas serão baixadas para a pasta especificada.

## Contribuições

Sinta-se à vontade para contribuir! Para isso, faça um fork deste repositório, crie sua branch com as modificações e envie um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
