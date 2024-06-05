import os
from mutagen.mp3 import MP3
from pydub import AudioSegment

# our files #
from more_functions import makedir


def get_mp3_duration(file_path):
    audio = MP3(file_path)
    duration_in_seconds = audio.info.length
    return duration_in_seconds


def cut_song(file_path, folder_name, type='song'):
    song = AudioSegment.from_mp3(file_path)
    duration = int(get_mp3_duration(file_path))
    path = rf'{os.getcwd()}\songs\{folder_name}\{type}_sections'
    makedir(path)
    print(f"Duration: {duration} seconds")
    second = 1000
    for i in range(duration):
        last = i - 1
        current_song = song[last * second:i * second]
        current_song.export(rf"{path}\sep_{i}.mp3", format="mp3")
    return path
