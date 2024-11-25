import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import pygame

def is_mp3_file(filename):
    return filename.lower().endswith('.mp3')

def import_playlist():
    global playlist, folder_path
    folder_path = filedialog.askdirectory(title="Select Folder Containing MP3 Files")
    if not folder_path:
        return
    mp3_files = [f for f in os.listdir(folder_path) if is_mp3_file(f)]
    if not mp3_files:
        messagebox.showerror("Import Error", "No MP3 files found in the selected folder.")
        return
    playlist.delete(0, tk.END)
    for mp3_file in mp3_files:
        playlist.insert(tk.END, mp3_file)
    messagebox.showinfo("Import Success", f"Successfully imported {len(mp3_files)} MP3 files.")

def play_selected_song():
    global folder_path
    selected_song_index = playlist.curselection()
    if not selected_song_index:
        messagebox.showwarning("Playback Error", "No song selected. Please select a song to play.")
        return
    selected_song = playlist.get(selected_song_index)
    song_path = os.path.join(folder_path, selected_song)
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    currently_playing.set(f"Playing: {selected_song}")

def stop_playback():
    pygame.mixer.music.stop()
    currently_playing.set("No song is currently playing.")

def create_gui():
    global playlist, currently_playing
    root = tk.Tk()
    root.title("AI Music Dj")
    root.geometry("400x400")

    tk.Label(root, text="Click the button below to import a playlist.").pack(pady=10)
    tk.Button(root, text="Import Playlist", command=import_playlist).pack(pady=10)

    playlist_frame = tk.Frame(root)
    playlist_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    playlist_scroll = tk.Scrollbar(playlist_frame, orient=tk.VERTICAL)
    playlist = Listbox(playlist_frame, yscrollcommand=playlist_scroll.set, selectmode=tk.SINGLE)
    playlist_scroll.config(command=playlist.yview)
    playlist_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    playlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    playback_frame = tk.Frame(root)
    playback_frame.pack(pady=10)
    tk.Button(playback_frame, text="Play", command=play_selected_song).grid(row=0, column=0, padx=5)
    tk.Button(playback_frame, text="Pause", command=stop_playback).grid(row=0, column=1, padx=5)

    currently_playing = tk.StringVar(value="No song is currently playing.")
    tk.Label(root, textvariable=currently_playing).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    playlist = None
    currently_playing = None
    folder_path = ""
    pygame.init()
    create_gui()
