import os
import librosa
import numpy as np
from pydub import AudioSegment
import scipy.io.wavfile as wavfile
from recognize_chord_name import find_chord
from more_functions import makedir, find_scale


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
    chords_path = process_audio(guitar_path, drums_stem)
    print("Segments and chords processed.")
    return chords_path


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


def build_arr_chords(segments, sr):
    recognized_chords = []
    arr_chord_to_filter = []
    for index, segment in enumerate(segments):
        seg_path = save_segment_to_wav(segment, sr, index)

        if not os.path.exists(seg_path):
            continue

        # Check if the segment is empty or contains negligible sound
        audio_data, sample_rate = librosa.load(seg_path, sr=None)
        if len(audio_data) == 0 or np.max(np.abs(audio_data)) < 0.01:
            print(f"Skipping empty or silent segment at index {index}")
            continue

        chord = find_chord(seg_path)
        segment_length = librosa.get_duration(y=audio_data, sr=sample_rate)
        arr_chord_to_filter.append(chord)
        recognized_chords.append({'name': chord, 'seconds': segment_length})
    arr_chord, scale, full_scale, index = find_scale(arr_chord_to_filter)
    file_path = rf'{os.getcwd()}\songs\{filename}\{filename}_chords.txt'

    with open(file_path, 'w') as file:
        ind = len(arr_chord)
        print(len(recognized_chords) - len(arr_chord))
        for i, ch in enumerate(recognized_chords):
            if i < ind:
                ch['name'] = arr_chord[i]
                file.write(f"{{ 'name': '{ch['name']}', 'seconds': {ch['seconds']} }},\n")

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
    return recognized_chords_path


guitar = r"C:\Users\User\Desktop\Guitutor\songs\Shmot_Hatzadikim\Shmot_Hatzadikim_acoustic_guitar_split_by_lalalai.mp3"
drums = r"C:\Users\User\Desktop\Guitutor\songs\Shmot_Hatzadikim\Shmot_Hatzadikim_vocal_drums.mp3"
split_by_drums_and_recognize_chords(guitar, drums, 'Shmot_Hatzadikim')
