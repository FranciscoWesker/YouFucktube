import pafy
import vlc
import time
import requests
from bs4 import BeautifulSoup

import youtube_dl

def buscar_videos(query):
    ydl_opts = {"default_search": "ytsearch10", "noplaylist": "True"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(query, download=False)["entries"]
    video_list = []
    if search_results:
        for result in search_results:
            if result.get("url"):
                video_list.append({
                    "title": result.get("title"),
                    "author": result.get("uploader"),
                    "duration": result.get("duration"),
                    "views": result.get("view_count"),
                    "rating": None,
                    "url": result.get("url")
                })
    return video_list


def reproducir_video(video_url):
    yt = YouTube(video_url)
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(output_path=".", filename="temp_audio")
    audio_path = "./temp_audio"
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new_path(audio_path)
    media.get_mrl()
    player.set_media(media)
    player.play()

    print(f"Reproduciendo: {yt.title}")
    while player.get_state() != vlc.State.Ended:
        time.sleep(1)


def main():
    print("""

 __   __        ___        _   _        _         
 \ \ / /__ _  _| __|  _ __| |_| |_ _  _| |__  ___ 
  \ V / _ \ || | _| || / _| / /  _| || | '_ \/ -_)
   |_|\___/\_,_|_| \_,_\__|_\_\\__|\_,_|_.__/\___|
                                                  

""")
    while True:
        query = input("Buscar (o 'q' para terminar): ")
        if query.lower() == "q":
            break

        video_list = buscar_videos(query)
        if video_list:
            print("Resultados de búsqueda:")
            for i, video_url in enumerate(video_list[:10]):
                yt = YouTube(video_url)
                print(f"{i + 1}. {yt.title}")

            seleccion = int(input("Seleccione el número del video para reproducir (o 0 para buscar de nuevo): "))
            if 1 <= seleccion <= 10:
                reproducir_video(video_list[seleccion - 1])
        else:
            print("No se encontraron resultados.")

if __name__ == "__main__":
    main()

