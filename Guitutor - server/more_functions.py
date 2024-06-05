import os
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks, fftconvolve


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
