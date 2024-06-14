import os
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks, fftconvolve

global scales
scales = {'Am': ['Em', 'Dm', 'G', 'F'],
          'C': ['G', 'F', 'Em', 'Dm'],
          'Em': ['Bm', 'Am', 'D', 'C'],
          'G': ['D', 'C', 'Bm', 'Am'],
          'Bm': ['F#m', 'Em', 'A', 'G'],
          'D': ['A', 'G', 'F#m', 'Em'],
          'F#m': ['C#m', 'Bm', 'E', 'D'],
          'A': ['E', 'D', 'C#m', 'Bm'],
          'C#m': ['G#m', 'F#m', 'B', 'A'],
          'E': ['B', 'A', 'G#m', 'F#m'],
          'G#m': ['Ebm', 'C#m', 'F', 'E'],
          'B': ['F', 'E', 'Ebm', 'C#m'],
          'Ebm': ['Bbm', 'G#m', 'C#', 'B'],
          'F#': ['C#', 'B', 'Bbm', 'G#m'],
          'C#': ['G#', 'B', 'Fm', 'Ebm'],
          'Bbm': ['Fm', 'Ebm', 'G#', 'B'],
          'G#': ['Eb', 'C#', 'Cm', 'Bbm'],
          'Fm': ['Cm', 'Bbm', 'Eb', 'C#'],
          'Eb': ['Bb', 'G#', 'Gm', 'Fm'],
          'Cm': ['Gm', 'Fm', 'Bb', 'G#'],
          'Bb': ['F', 'Eb', 'Dm', 'Cm'],
          'Gm': ['Dm', 'Cm', 'F', 'Eb'],
          'F': ['C', 'Bb', 'Am', 'Gm'],
          'Dm': ['Am', 'Gm', 'C', 'Bb']}


def find_harmonics(path, print_peaks=False):
    fs, X = wavfile.read(path)
    # Check if the audio file is stereo (2 channels)
    if X.ndim > 1:
        # X is stereo, average the channels to make it mono
        X = X.mean(axis=1)
    N = len(X)
    X_F = fft(X)
    X_F_onesided = 2.0 / N * np.abs(X_F[0:N // 2])
    freqs = fftfreq(N, 1 / fs)[:N // 2]
    freqs_50_index = np.abs(freqs - 50).argmin()
    h = X_F_onesided.max() * 5 / 100
    peaks, _ = find_peaks(X_F_onesided, distance=10, height=h)
    peaks = peaks[peaks > freqs_50_index]
    harmonics = np.round(freqs[peaks], 2)
    return harmonics


def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def convert_to_wav(file, output_dir):
    file_name, file_extension = os.path.splitext(file)

    # Convert to WAV if the file is MP3
    if file_extension.lower() != ".wav":
        audio = AudioSegment.from_mp3(file)
        wav_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file))[0] + ".wav")
        audio.export(wav_file, format="wav")
        return wav_file
    else:
        return file


def compare_chords(ch_song, ch_user):
    pass


def find_scale(chord_file_arr):
    Am_scale = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    minor_scale = ['m', '', '', 'm', 'm', '', '']
    cols = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]
    # become the arr to a dictionary sort by values:
    a = np.array(chord_file_arr)
    unique, counts = np.unique(a, return_counts=True)
    dict_before_sort = dict(zip(unique, counts))
    sort_dict = {k: v for k, v in sorted(dict_before_sort.items(), key=lambda item: item[1], reverse=True)}
    merge_dict = {}
    for item in sort_dict.keys():
        for i in sort_dict.keys():
            if item != i and item[0] == i[0]:
                if 'b' in item and 'b' not in i:
                    continue
                elif 'b' not in item and 'b' in i:
                    continue
                if '#' in item and '#' not in i:
                    continue
                elif '#' not in item and '#' in i:
                    continue
                elif sort_dict[i] > sort_dict[item]:
                    merge_dict[i, item] = sort_dict[i], sort_dict[item], sort_dict[i] + sort_dict[item]
                elif sort_dict[item] > sort_dict[i]:
                    merge_dict[item, i] = sort_dict[i], sort_dict[item], sort_dict[i] + sort_dict[item]

    merge_dict = {k: v for k, v in sorted(merge_dict.items(), key=lambda item: item[1][2], reverse=True)}

    arr_scale = {}
    ind = 0
    for item in merge_dict.keys():
        if ind < 6:
            arr_scale[item] = merge_dict[item]
            ind += 1
    # send to function that find the scales
    scale = scale_is(arr_scale)
    # find the exact scale
    true_scale = []
    for s in scale.keys():
        max_false = 0
        if scale[s][1].index('False') > max_false:
            max_false = scale[s][1].index('False')
            true_scale = s, scale[s][0]
    full_scale = []
    if 'm' in true_scale[0]:
        ind = cols.index(true_scale[0][:-1])
        for i in range(7):
            c = cols.index(Am_scale[i])
            c = (c + ind) % 12
            full_scale.append(f'{cols[c]}{minor_scale[i]}')
    else:
        ind = cols.index(true_scale[0])
        for i in range(7):
            c = cols.index(Am_scale[i])+3
            c = (c + ind) % 12
            full_scale.append(f'{cols[c]}{minor_scale[i]}')
    print(ind, full_scale)
    count = 0
    new_txt = []
    for c in chord_file_arr:
        if c in full_scale:
            new_txt.append(c)
        elif 'm' in c:
            if c[:-1] in full_scale:
                new_txt.append(c[:-1])
        elif c+'m' in full_scale:
            new_txt.append(c+'m')
        else:
            count += 1
            new_txt.append('None')

    return new_txt, true_scale[0], full_scale, ind+1


def scale_is(arr_scale):
    print(arr_scale)
    compare_result = {}
    index = 0
    for item in arr_scale.keys():
        if index > 1:
            break
        else:
            num_chords_in_scale = 0
            # print('new iterate')
            a_ = []
            index += 1
            if len(item) > 1:
                for i in scales.keys():
                    if item[0] == i:
                        bool_arr = ['False', 'False', 'False', 'False']
                        for it in arr_scale.keys():
                            for minor_or_major in it:
                                if minor_or_major in scales[i]:
                                    ind = scales[i].index(minor_or_major)
                                    bool_arr[ind] = 'True'
                                    a_ = scales[i], bool_arr
                                    num_chords_in_scale += 1
                        # if num_chords_in_scale > 2:
                        compare_result[item[0]] = a_

                for i in scales.keys():
                    if item[1] == i:
                        bool_arr = ['False', 'False', 'False', 'False']
                        for it in arr_scale.keys():
                            for minor_or_major in it:
                                if minor_or_major in scales[i]:
                                    ind = scales[i].index(minor_or_major)
                                    bool_arr[ind] = 'True'
                                    num_chords_in_scale += 1
                                    a_ = scales[i], bool_arr
                        # if num_chords_in_scale > 2:
                        compare_result[item[1]] = a_
            else:
                for i in scales.keys():
                    if item == i:
                        bool_arr = ['False', 'False', 'False', 'False']
                        for it in arr_scale.keys():
                            for minor_or_major in it:
                                if minor_or_major in scales[i]:
                                    ind = scales[i].index(minor_or_major)
                                    bool_arr[ind] = 'True'
                                    num_chords_in_scale += 1
                                    a_ = scales[i], bool_arr
                        # if num_chords_in_scale > 2:
                        compare_result[item] = a_
    return compare_result


def read_file_into_array(file_path: str) -> list:
    array = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip newline character and split by comma
            data = line.strip().split(', ')
            array.append(data)
    return array


