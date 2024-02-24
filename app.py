import os, signal, time, requests
from urllib.parse import urlparse, parse_qs
from colorama import init, Fore, Back #  colorama
from pytube import YouTube #  pytube
from tqdm import tqdm # tqdm
from moviepy.editor import * # moviepy

init()
os.system("cls")

print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + "Modo de uso:\n")
print(" 1. modo de consola " + Fore.LIGHTBLACK_EX + "url o urls + espacios\n" + Fore.RESET)
print(" 2. modo de archivo " + Fore.LIGHTBLACK_EX + "urls en el links.txt\n")

# ctrl c

def ctrl_C(signum, frame):
    print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + "Saliendo...")
    exit(1)

signal.signal(signal.SIGINT, ctrl_C)

mode = 0
#selecciona el modo de utilizasión
def selectMode():
    global mode
    modeSelected = input(Back.BLACK + Fore.WHITE + " " + "¿1 o 2?" + " " + Fore.BLACK + Back.RESET + "\ue0b0 " + Fore.WHITE)
    if modeSelected == "1":
        mode = 1
    elif modeSelected == "2":
        mode = 2
    else:
        print(Fore.LIGHTBLUE_EX + "\n[App]: " + Fore.RED + "Error\n")

# crea los directorios y archivos necesarios

def setup():
    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    if not os.path.exists("downloads_converted"):
        os.mkdir("downloads_converted")
    
    if not os.path.exists("links.txt"):
        with open("links.txt", "w") as f:
            f.write("")

setup()
selectMode()

#validador de url de youtube
def validate_youtube_urls(urls):
    valid_urls = []
    for url in urls:
        # Verificar si es una URL de YouTube
        parsed_url = urlparse(url)
        if parsed_url.netloc != 'www.youtube.com' or parsed_url.path != '/watch':
            print("1")
            print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.BLUE + f"{url} " + Fore.RED + "No es una url de youtube")
            continue
        
        # Obtener el ID del video
        video_id = parse_qs(parsed_url.query)['v'][0]
        print(video_id)
        
        # Verificar si el video existe
        response = requests.get(f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}")
        if response.status_code != 200:
            print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.BLUE + f"{url} " + Fore.RED + "El video no existe")
            print("2")
            continue
        
        # Si llegamos hasta aquí, la URL es válida y el video existe
        print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.BLUE + f"{url} " + Fore.GREEN + "El video existe")
        valid_urls.append(url)
    
    return valid_urls

#descarga los videos o video

def download_videos(urls, download_dir):
    for url in urls:
        try:
            # Crear objeto YouTube y obtener la mayor calidad disponible
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            
            # Descargar el video y mostrar barra de progreso
            print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + f"Descargando {yt.title}...")
            
            stream.download(download_dir)
            
            print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.GREEN + f"{yt.title} descargado exitosamente!")
        except Exception as e:
            print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.RED + f"Ocurrió un error al descargar {url}: {e}")
    
    print(Fore.LIGHTBLUE_EX + "\n[App]: " + Fore.WHITE + f"Se descargaron {len(urls)} videos exitosamente!")

# modo 1 (consola)
if mode == 1:
    os.system("cls")
    print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + "Proporsione una url o varias separadas con espacios\n")
    time.sleep(1)
    urls = input(Back.BLACK + Fore.WHITE + " " + "¿url|urls?" + " " + Fore.BLACK + Back.RESET + "\ue0b0 " + Fore.WHITE).split()
    print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + "Validando...\n")
    valid_urls = validate_youtube_urls(urls)
    
    # Crear carpeta de descargas si no existe
    download_dir = "downloads"
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    # Verificar si hay archivos en la carpeta de descargas
    existing_files = os.listdir(download_dir)
    if existing_files:
        print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + "Hay archivos en la carpeta de descargas. ¿Desea eliminarlos? (s/n)\n")
        response = input(Back.BLACK + Fore.WHITE + " " + "¿s o n?" + " " + Fore.BLACK + Back.RESET + "\ue0b0 " + Fore.WHITE)
        if response.lower() == 's':
            for file in existing_files:
                os.remove(os.path.join(download_dir, file))
        else:
            print("")
    # ! añadir [contador] yt.title en filename sin joder el codigo entero
    # * todo es culpa de la s de yt.titles
    
    download_videos(valid_urls, download_dir)
    print(Fore.LIGHTBLUE_EX + "\n[App]: " + Fore.WHITE + "¿Convertir a mp3?\n")
    convert = input(Back.BLACK + Fore.WHITE + "¿s o n?" + " " + Fore.BLACK + Back.RESET + "\ue0b0 " + Fore.WHITE)
    # convierte el video si el usuario lo desea
    if convert == "s":
        mp4_files = [f for f in os.listdir("./downloads/") if f.endswith('.mp4')]
        for mp4_file in mp4_files:
            mp4_path = os.path.join("./downloads/", mp4_file)
            mp3_file = mp4_file[:-4] + '.mp3'
            mp3_path = os.path.join("./downloads_converted/", mp3_file)
            video = VideoFileClip(mp4_path)
            audio = video.audio
            audio.write_audiofile(mp3_path)
            audio.close()
            video.close()
        else: print(Fore.LIGHTBLUE_EX + "\n[App]: " + Fore.WHITE + "Saliendo...")


# modo 2 (links.txt)
if mode == 2:
    os.system("cls")
    print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + "Validando...\n")
    time.sleep(1)
    with open("links.txt") as archivo:
        urls = archivo.readlines()
    valid_urls = validate_youtube_urls(urls)
    
    # Crear carpeta de descargas si no existe
    download_dir = "downloads"
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    
    # Verificar si hay archivos en la carpeta de descargas
    existing_files = os.listdir(download_dir)
    if existing_files:
        print(Fore.LIGHTBLUE_EX + "[App]: " + Fore.WHITE + "Hay archivos en la carpeta de descargas. ¿Desea eliminarlos? (s/n)\n")
        response = input(Back.BLACK + Fore.WHITE + " " + "¿s o n?" + " " + Fore.BLACK + Back.RESET + "\ue0b0 " + Fore.WHITE)
        if response.lower() == 's':
            for file in existing_files:
                os.remove(os.path.join(download_dir, file))
        else:
            print("error")
    download_videos(valid_urls, download_dir)
    print(Fore.LIGHTBLUE_EX + "\n[App]: " + Fore.WHITE + "¿Convertir a mp3?\n")
    convert = input(Back.BLACK + Fore.WHITE + " " + "¿s o n?" + " " + Fore.BLACK + Back.RESET + "\ue0b0 " + Fore.WHITE)
    if convert == "s":
        mp4_files = [f for f in os.listdir("./downloads/") if f.endswith('.mp4')]
        for mp4_file in mp4_files:
            mp4_path = os.path.join("./downloads/", mp4_file)
            mp3_file = mp4_file[:-4] + '.mp3'
            mp3_path = os.path.join("./downloads_converted/", mp3_file)
            video = VideoFileClip(mp4_path)
            audio = video.audio
            audio.write_audiofile(mp3_path)
            audio.close()
            video.close()
        else: print(Fore.LIGHTBLUE_EX + "\n[App]: " + Fore.WHITE + "Saliendo...")

