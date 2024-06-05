import os

import librosa
import numpy as np
from pydub import AudioSegment
import scipy.io.wavfile as wavfile
from recognize_chord_name import find_chord
from more_functions import makedir


def split_by_drums_and_recognize_chords(drums_path, guitar_path, fname):
    global filename
    filename = fname
    # Separate the stems,
    drums_stem, sr = librosa.load(drums_path)
    # Detect drum beats
    tempo, beats = librosa.beat.beat_track(y=drums_stem, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    print("Detected beats at times (seconds):",
          beat_times)  # Function to separate stems (implement or use your existing function)
    # Load the audio file into a pydub AudioSegment for easy slicing
    # audio_segment = AudioSegment.from_file(guitar_path)
    # segments = create_segments(audio_segment, beat_times)
    chords_path = process_audio(guitar_path, drums_stem)
    print("Segments and chords processed.")
    return chords_path


# def separate_stems(other_path):
#     y, sr = librosa.load(other_path, sr=None)
#     return y, sr

# Function to convert librosa time to pydub milliseconds
def time_to_ms(time):
    return int(time * 1000)


# Create segments based on beat times and return as numpy arrays
def create_segments(audio_segment, beat_times):
    segments = []
    for i in range(len(beat_times) - 1):
        start_time = time_to_ms(beat_times[i])
        end_time = time_to_ms(beat_times[i + 1])
        segment = audio_segment[start_time:end_time]
        segment_array = np.array(segment.get_array_of_samples()).reshape(-1, audio_segment.channels)
        segments.append(segment_array)

    # Handle the last segment (from the last beat to the end of the audio)
    if beat_times[-1] < len(audio_segment) / 1000.0:
        start_time = time_to_ms(beat_times[-1])
        segment = audio_segment[start_time:]
        segment_array = np.array(segment.get_array_of_samples()).reshape(-1, audio_segment.channels)
        segments.append(segment_array)

    return segments


# Recognize chords for each segment
def build_arr_chords(segments, sr):
    recognized_chords = []
    for index, segment in enumerate(segments):
        seg_path = save_segment_to_wav(segment, sr, index)

        if not os.path.exists(seg_path):
            continue

        # Check if the segment is empty or contains negligible sound
        audio_data, sample_rate = librosa.load(seg_path, sr=None)
        if len(audio_data) == 0 or np.max(np.abs(audio_data)) < 0.01:
            print(f"Skipping empty or silent segment at index {index}")
            continue

        chord, i = find_chord(seg_path)
        recognized_chords.append(chord)
        print(f"Recognized chord: {chord}")
    file_path = rf'{os.getcwd()}\songs\{filename}\{filename}_chords.txt'
    with open(file_path, 'w') as file:
        for ch in recognized_chords:
            file.write(f'{ch}, ')
    print(recognized_chords)
    return file_path


def save_segment_to_wav(segment, sr, i):
    s_path = os.path.join(os.getcwd(), 'songs', filename, 'segments')

    # Ensure the directory exists
    if not os.path.exists(s_path):
        try:
            os.makedirs(s_path)
        except PermissionError as e:
            print(f"Permission denied: {e}")
            return None
        except OSError as e:
            print(f"Error creating directory: {e}")
            return None

    file_path = os.path.join(s_path, f'{i}.wav')
    try:
        wavfile.write(file_path, sr, segment)
    except PermissionError as e:
        print(f"Permission denied when writing file: {e}")
        return None
    except OSError as e:
        print(f"Error writing file: {e}")
        return None

    return file_path


# Example usage:
# segment = segments[0]  # Using the first segment for example
# save_segment_to_wav(segment, sr, "output_segment.wav")

# Example: returning segments and recognized chords
def process_audio(guitar_path, drum_stem):
    y, sr = librosa.load(guitar_path, sr=None)
    # drum_stem = drums_stem
    tempo, beats = librosa.beat.beat_track(y=drum_stem, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    audio_segment = AudioSegment.from_file(guitar_path)
    segments = create_segments(audio_segment, beat_times)

    recognized_chords_path = build_arr_chords(segments, sr)

    # recognized_chords = []
    # for segment in segments:
    #     chord = recognize_chord(segment)
    #     recognized_chords.append(chord)
    return recognized_chords_path


# Example usage
# Load the audio file
drums = r"C:\Users\User\Desktop\Guitutor\songs\baavur\drumss.mp3"
other = r"C:\Users\User\Desktop\Guitutor\songs\baavur\guitar.mp3"
path = split_by_drums_and_recognize_chords(drums, other, 'baavur')
