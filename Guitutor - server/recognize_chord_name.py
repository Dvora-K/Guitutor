# import IPython
# import numpy as np
# import pandas as pd
# from scipy.io import wavfile
# from scipy.fft import fft, fftfreq
# from scipy.signal import find_peaks, fftconvolve
# # from pydub import AudioSegment
# # import IPython
# # import seaborn as sns
# # our files #
# from more_functions import convert_to_wav
# from prediction_from_model import get_prediction
# from more_functions import find_harmonics
#
#
# # from build_chord_classifcation_model_rfc import find_harmonics
#
#
# def create_data_frame_freq():
#     # Our hearing range is commonly 20 Hz to 20 kHz
#     # Starting with 55 Hz which is "A" (I divided 440 by 2 three times)
#     curr_freq = 55
#     freq_list = []
#
#     # I want to calculate 8 octaves of notes. Each octave has 12 notes. Looping for 96 steps:
#     for i in range(96):
#         freq_list.append(curr_freq)
#         curr_freq *= np.power(2, 1 / 12)  # Multiplying by 2^(1/12)
#
#     # reshaping and creating dataframe
#     freq_array = np.reshape(np.round(freq_list, 1), (8, 12))
#     cols = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
#     df_note_freqs = pd.DataFrame(freq_array, columns=cols)
#
#     print("NOTE FREQUENCIES IN WESTERN MUSIC")
#     df_note_freqs.head(10)
#
#     return cols, df_note_freqs
#
#
# def find_value_of_one_note(note):
#     cols, df_note_freqs = create_data_frame_freq()
#     octav = 1
#     note_number = 0
#     freq = 55
#     note_hertz = 0
#     basic_note = note  # 440
#     while (basic_note > 110):
#         basic_note /= 2
#         octav += 1  # 3
#     while (freq * np.power(2, 1 / 12) < basic_note):
#         freq *= np.power(2, 1 / 12)
#         note_number += 1
#     freq_after = freq * np.power(2, 1 / 12)
#     if (basic_note - freq > freq_after - basic_note):
#         note_number += 1
#         if note_number == 12:
#             note_number = 0
#             octav += 1
#         exact_base_key = freq_after
#         note_hertz = freq_after * np.power(2, octav - 1)
#     else:
#         exact_base_key = freq
#     note_hertz = df_note_freqs.iloc[octav - 1, note_number]
#     note_name = cols[note_number]
#     note_details = {
#         "basic_note": basic_note,
#         "octave": octav,
#         "note_number": note_number,
#         "note_name": note_name,
#         "note_hertz": note_hertz
#     }
#     return note_details
#
#
# def find_chord(path):
#     wav_path = convert_to_wav(path, '.')
#     arr_harmonics = find_harmonics(wav_path)
#     print("arr", arr_harmonics)
#     note_0 = find_value_of_one_note(arr_harmonics[0])
#     notes_arr = []
#     basic_octave = note_0["octave"]
#     print("first note: " + note_0["note_name"], note_0["basic_note"])
#
#     harmonic_chord_arr = []
#     print("basic_octave: ", basic_octave)
#     print("arr_harmonics: ", arr_harmonics)
#
#     for i, h in enumerate(arr_harmonics):
#         n = find_value_of_one_note(h)
#         notes_arr.append(n)
#         if n["note_name"] not in harmonic_chord_arr:
#             harmonic_chord_arr.append(n["note_name"])
#     print("harmonic_chord_arr: ", harmonic_chord_arr)
#     type_chord = get_prediction(path)
#     for note_x in notes_arr:
#         if is_the_chord_by_this_note(note_x, harmonic_chord_arr, type_chord):
#             return f"{note_x["note_name"]} {type_chord}"
#     return 'None'
#
#
# def build_chords_name_and_arr(note_x, type_chord):
#     build_chord_arr = []
#     build_chord_name = []
#     cols, df_note_freqs = create_data_frame_freq()
#     if type_chord == 'Minor':
#         print('minor')
#         build_chord_arr = [note_x["note_number"], note_x["note_number"] + 3, note_x["note_number"] + 7]
#         build_chord_name = [cols[note_x["note_number"]], cols[(note_x["note_number"] + 3) % 12],
#                             cols[(note_x["note_number"] + 7) % 12]]
#     elif type_chord == 'Major':
#         print('major')
#         build_chord_arr = [note_x["note_number"], note_x["note_number"] + 4, note_x["note_number"] + 7]
#         build_chord_name = [cols[note_x["note_number"]], cols[(note_x["note_number"] + 4) % 12],
#                             cols[(note_x["note_number"] + 7) % 12]]
#     return build_chord_arr, build_chord_name
#
#
# def is_the_chord_by_this_note(note_x, harmonic_chord_arr,type_chord):
#     print(type_chord)
#     print('model success')
#     build_chord_arr, build_chord_name = build_chords_name_and_arr(note_x, type_chord)
#     if build_chord_name[0] in harmonic_chord_arr and build_chord_name[1] in harmonic_chord_arr and build_chord_name[
#         2] in harmonic_chord_arr:
#         return True, type_chord
#     return False
#
# # path = r"C:\Users\User\Desktop\Guitutor\songs\record.mp3"
# # print(find_chord(path))
# import IPython
import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks, fftconvolve
from pydub import AudioSegment
import IPython
import seaborn as sns
# our files #
from more_functions import convert_to_wav
from prediction_from_model import get_prediction
from more_functions import find_harmonics


# from build_chord_classifcation_model_rfc import find_harmonics


def create_data_frame_freq():
    # Our hearing range is commonly 20 Hz to 20 kHz
    # Starting with 55 Hz which is "A" (I divided 440 by 2 three times)
    curr_freq = 55
    freq_list = []

    # I want to calculate 8 octaves of notes. Each octave has 12 notes. Looping for 96 steps:
    for i in range(96):
        freq_list.append(curr_freq)
        curr_freq *= np.power(2, 1 / 12)  # Multiplying by 2^(1/12)

    # reshaping and creating dataframe
    freq_array = np.reshape(np.round(freq_list, 1), (8, 12))
    # cols = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    cols = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]
    df_note_freqs = pd.DataFrame(freq_array, columns=cols)

    df_note_freqs.head(10)

    return cols, df_note_freqs


# def find_value_of_one_note(note):
#     cols, df_note_freqs = create_data_frame_freq()
#     print(df_note_freqs)
#     octav = 1
#     note_number = 0
#     freq = 55
#     note_hertz = 0
#     basic_note = note  # 440
#     while (basic_note > 110):
#         basic_note /= 2
#         octav += 1  # 3
#     while (freq * np.power(2, 1 / 12) < basic_note):
#         freq *= np.power(2, 1 / 12)
#         note_number += 1
#     freq_after = freq * np.power(2, 1 / 12)
#     if (basic_note - freq > freq_after - basic_note):
#         note_number += 1
#         if note_number == 12:
#             note_number = 0
#             octav += 1
#         exact_base_key = freq_after
#         note_hertz = freq_after * np.power(2, octav - 1)
#     else:
#         exact_base_key = freq
#     print("octav", octav, "notenum:", note_number)
#     note_hertz = df_note_freqs.iloc[octav - 1, note_number]
#     note_name = cols[note_number]
#     note_details = {
#         "basic_note": basic_note,
#         "octave": octav,
#         "note_number": note_number,
#         "note_name": note_name,
#         "note_hertz": note_hertz
#     }
#     return note_details
def find_value_of_one_note(note):
    cols, df_note_freqs = create_data_frame_freq()
    octav = 1
    note_number = 0
    freq = 55
    note_hertz = 0
    basic_note = note  # 440
    while basic_note > 110:
        basic_note /= 2
        octav += 1  # 3
    while freq * np.power(2, 1 / 12) < basic_note:
        freq *= np.power(2, 1 / 12)
        note_number += 1
    freq_after = freq * np.power(2, 1 / 12)
    if basic_note - freq > freq_after - basic_note:
        note_number += 1
        if note_number == 12:
            note_number = 0
            octav += 1
        exact_base_key = freq_after
        note_hertz = freq_after * np.power(2, octav - 1)
    else:
        exact_base_key = freq
    if octav > 8:
        octav = 8
    try:
        note_hertz = df_note_freqs.iloc[octav - 1, note_number % 12]
        note_name = cols[note_number]
        note_details = {
            "basic_note": basic_note,
            "octave": octav,
            "note_number": note_number,
            "note_name": note_name,
            "note_hertz": note_hertz
        }
    except Exception as e:
        print(f"Exception: {e}")
        return None
    return note_details


def find_chord(path):
    wav_path = convert_to_wav(path, '.')
    arr_harmonics = find_harmonics(wav_path)
    print("arr", arr_harmonics)
    note_0 = find_value_of_one_note(arr_harmonics[0])
    notes_arr = []
    basic_octave = note_0["octave"]
    harmonic_chord_arr = []
    for i, h in enumerate(arr_harmonics):
        n = find_value_of_one_note(h)
        notes_arr.append(n)
        if n["note_name"] not in harmonic_chord_arr:
            harmonic_chord_arr.append(n["note_name"])
    type_chord = get_prediction(path)
    for note_x in notes_arr:
        print("note_x:", note_x, "harmonic_chord_arr:", harmonic_chord_arr, "type_chord:", type_chord)
        if is_the_chord_by_this_note(note_x, harmonic_chord_arr, type_chord):
            if type_chord == 'Minor':
                return f"{note_x['note_name']}m"
            else:
                return note_x['note_name']
    return 'None'


def build_chords_name_and_arr(note_x, type_chord):
    build_chord_arr = []
    build_chord_name = []
    cols, df_note_freqs = create_data_frame_freq()
    if type_chord == 'Minor':
        build_chord_arr = [note_x["note_number"], note_x["note_number"] + 3, note_x["note_number"] + 7]
        build_chord_name = [cols[note_x["note_number"]], cols[(note_x["note_number"] + 3) % 12],
                            cols[(note_x["note_number"] + 7) % 12]]
    elif type_chord == 'Major':
        build_chord_arr = [note_x["note_number"], note_x["note_number"] + 4, note_x["note_number"] + 7]
        build_chord_name = [cols[note_x["note_number"]], cols[(note_x["note_number"] + 4) % 12],
                            cols[(note_x["note_number"] + 7) % 12]]
    return build_chord_arr, build_chord_name


def is_the_chord_by_this_note(note_x, harmonic_chord_arr, type_chord):
    try:
        build_chord_arr, build_chord_name = build_chords_name_and_arr(note_x, type_chord)
        if (build_chord_name[0] in harmonic_chord_arr and build_chord_name[1] in harmonic_chord_arr and
                build_chord_name[2]
                in harmonic_chord_arr):
            return True, type_chord
    except IndexError as e:
        print(f"IndexError in build_chord_name: {e} ")
        return None
    return False
