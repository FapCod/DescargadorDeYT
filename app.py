import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import Playlist, YouTube
from pydub import AudioSegment

# Establecer las rutas a ffmpeg y ffprobe
def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "ffmpeg", "ffmpeg.exe")
    return os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")

def get_ffprobe_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "ffmpeg", "ffprobe.exe")
    return os.path.join(os.getcwd(), "ffmpeg", "ffprobe.exe")

AudioSegment.converter = get_ffmpeg_path()
AudioSegment.ffprobe = get_ffprobe_path()

def download_youtube_video(video_url, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        yt = YouTube(video_url)
        video_stream = yt.streams.filter(only_audio=True).first()
        progress_bar["maximum"] = 100

        def progress_callback(stream, chunk, bytes_remaining):
            filesize = stream.filesize
            bytes_downloaded = filesize - bytes_remaining
            percentage = (bytes_downloaded / filesize) * 100
            progress_bar["value"] = percentage
            root.update_idletasks()

        yt.register_on_progress_callback(progress_callback)
        audio_file = video_stream.download(output_path=output_folder)

        base, ext = os.path.splitext(audio_file)
        mp3_file = f"{base}.mp3"
        audio = AudioSegment.from_file(audio_file)
        audio.export(mp3_file, format="mp3")
        os.remove(audio_file)

        progress_bar["value"] = 100
        root.update_idletasks()
        messagebox.showinfo("Éxito", "Descarga completada y archivo convertido a MP3")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar el video: {e}")

def download_youtube_playlist(playlist_url, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        playlist = Playlist(playlist_url)
        num_videos = len(playlist.video_urls)
        progress_bar["maximum"] = num_videos

        for index, video_url in enumerate(playlist.video_urls):
            yt = YouTube(video_url)
            video_stream = yt.streams.filter(only_audio=True).first()
            audio_file = video_stream.download(output_path=output_folder)

            base, ext = os.path.splitext(audio_file)
            mp3_file = f"{base}.mp3"
            audio = AudioSegment.from_file(audio_file)
            audio.export(mp3_file, format="mp3")
            os.remove(audio_file)

            progress_bar["value"] = index + 1
            root.update_idletasks()

        messagebox.showinfo("Éxito", "Descarga completada y archivos convertidos a MP3")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar la lista de reproducción: {e}")

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_selected)

def start_download_playlist():
    playlist_url = playlist_url_entry.get()
    output_folder = output_folder_entry.get()

    if not playlist_url:
        messagebox.showwarning("Advertencia", "Por favor, introduce la URL de la lista de reproducción")
        return

    if not output_folder:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta de salida")
        return

    download_youtube_playlist(playlist_url, output_folder)

def start_download_video():
    video_url = video_url_entry.get()
    output_folder = output_folder_entry.get()

    if not video_url:
        messagebox.showwarning("Advertencia", "Por favor, introduce la URL del video")
        return

    if not output_folder:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta de salida")
        return

    download_youtube_video(video_url, output_folder)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("Descarga de YouTube a MP3 By FapCod")

tk.Label(root, text="URL de la Lista de Reproducción de YouTube:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
playlist_url_entry = tk.Entry(root, width=50)
playlist_url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="URL del Video de YouTube:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
video_url_entry = tk.Entry(root, width=50)
video_url_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Carpeta de Salida:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=2, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Examinar...", command=browse_output_folder)
browse_button.grid(row=2, column=2, padx=10, pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

download_playlist_button = tk.Button(root, text="Descargar Lista de Reproducción", command=start_download_playlist)
download_playlist_button.grid(row=4, column=0, columnspan=3, pady=10)

download_video_button = tk.Button(root, text="Descargar Video", command=start_download_video)
download_video_button.grid(row=5, column=0, columnspan=3, pady=10)

center_window(root)
root.mainloop()
