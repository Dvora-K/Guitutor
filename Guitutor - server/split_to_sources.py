import torch
import torchaudio
import matplotlib.pyplot as plt
import os
import wavio
from pydub import AudioSegment
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS
from torchaudio.utils import download_asset
from torchaudio.transforms import Fade

print(torch.__version__)
print(torchaudio.__version__)

# important definitions

bundle = HDEMUCS_HIGH_MUSDB_PLUS

model = bundle.get_model()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model.to(device)

sample_rate = bundle.sample_rate

print(f"Sample rate: {sample_rate}")


# model:

def separate_sources(
        model,
        mix,
        segment=10.0,
        overlap=0.1,
        device=None,
):
    """
    Apply model to a given mixture. Use fade, and add segments together in order to add model segment by segment.

    Args:
        segment (int): segment length in seconds
        device (torch.device, str, or None): if provided, device on which to
            execute the computation, otherwise `mix.device` is assumed.
            When `device` is different from `mix.device`, only local computations will
            be on `device`, while the entire tracks will be stored on `mix.device`.
    """
    if device is None:
        device = mix.device
    else:
        device = torch.device(device)

    batch, channels, length = mix.shape

    chunk_len = int(sample_rate * segment * (1 + overlap))
    start = 0
    end = chunk_len
    overlap_frames = overlap * sample_rate
    fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")

    final = torch.zeros(batch, len(model.sources), channels, length, device=device)

    while start < length - overlap_frames:
        chunk = mix[:, :, start:end]
        with torch.no_grad():
            out = model.forward(chunk)
        out = fade(out)
        final[:, :, :, start:end] += out
        if start == 0:
            fade.fade_in_len = int(overlap_frames)
            start += int(chunk_len - overlap_frames)
        else:
            start += chunk_len
        end += chunk_len
        if end >= length:
            fade.fade_out_len = 0
    return final


def plot_spectrogram(stft, title="Spectrogram"):
    magnitude = stft.abs()
    spectrogram = 20 * torch.log10(magnitude + 1e-8).numpy()
    _, axis = plt.subplots(1, 1)
    axis.imshow(spectrogram, cmap="viridis", vmin=-60, vmax=0, origin="lower", aspect="auto")
    axis.set_title(title)
    plt.tight_layout()


# run model:

# We download the audio file from our storage. Feel free to download another file and use audio from a specific path
def load_song(song_router):
    # SAMPLE_SONG = download_asset(song_router)
    # waveform, sample_rate = torchaudio.load(SAMPLE_SONG)  # replace SAMPLE_SONG with desired path for different song
    #
    # waveform = waveform.to(device)
    # mixture = waveform
    #
    # # parameters
    # segment: int = 10
    # overlap = 0.1
    #
    # print("Separating track")
    # ref = waveform.mean(0)
    # waveform = (waveform - ref.mean()) / ref.std()  # normalization
    # global sources
    # sources = separate_sources(
    #     model,
    #     waveform[None],
    #     device=device,
    #     segment=segment,
    #     overlap=overlap,
    # )[0]
    #
    # sources = sources * ref.std() + ref.mean()
    # sources_list = model.sources
    #
    # sources = list(sources)
    # print(sources_list)
    # audios = dict(zip(sources_list, sources))
    # return sources
    SAMPLE_SONG = song_router
    waveform, sample_rate = torchaudio.load(SAMPLE_SONG)  # replace SAMPLE_SONG with desired path for different song

    # Ensure the waveform is in stereo
    if waveform.size(0) == 1:  # If the audio is mono (single channel)
        waveform = waveform.repeat(2, 1)  # Convert mono to stereo by repeating the channel

    waveform = waveform.to(device)
    mixture = waveform

    # parameters
    segment: int = 10
    overlap = 0.1

    print("Separating track")
    ref = waveform.mean(0)
    waveform = (waveform - ref.mean()) / ref.std()  # normalization
    global sources
    sources = separate_sources(
        model,
        waveform[None],
        device=device,
        segment=segment,
        overlap=overlap,
    )[0]

    sources = sources * ref.std() + ref.mean()
    sources_list = model.sources

    sources = list(sources)
    print(sources_list)
    audios = dict(zip(sources_list, sources))
    return sources


def build_vocal(file, mode='upload'):
    directory = rf"{os.getcwd()}\songs\{file}"
    if mode == 'record':
        directory = rf"{os.getcwd()}\songs\{file}\user"
    # Write the vocal file
    wavio.write(rf"{directory}\{file}_vocal.wav", sources[3][0] + sources[3][1], sample_rate, sampwidth=2)
    # Convert to mp3
    sound = AudioSegment.from_wav(rf"{directory}\{file}_vocal.wav")
    sound.export(rf"{directory}\{file}_vocal.mp3", format='mp3')
    # Remove the temporary wav file
    os.remove(rf"{directory}\{file}_vocal.wav")


def build_drums(file, mode='upload'):
    # Define the directory path
    directory = rf"{os.getcwd()}\songs\{file}"
    if mode == 'record':
        directory = rf"{os.getcwd()}\songs\{file}\user"
    # Write the vocal file
    wavio.write(rf"{directory}\{file}_drums.wav", sources[0][0] + sources[0][1], sample_rate, sampwidth=2)
    # Convert to mp3
    sound = AudioSegment.from_wav(rf"{directory}\{file}_drums.wav")
    sound.export(rf"{directory}\{file}_drums.mp3", format='mp3')
    # Remove the temporary wav file
    os.remove(rf"{directory}\{file}_drums.wav")
    return rf"{directory}\{file}_drums.mp3"


def build_bass(file, mode='upload'):
    directory = rf"{os.getcwd()}\songs\{file}"
    if mode == 'record':
        directory = rf"{os.getcwd()}\songs\{file}\user"
    wavio.write(rf"{directory}\{file}_bass.wav", sources[1][0] + sources[1][1], sample_rate, sampwidth=2)
    sound = AudioSegment.from_wav(rf"{directory}\{file}_bass.wav")
    sound.export(rf"{directory}\{file}_bass.mp3", format='mp3')
    os.remove(rf"{directory}\{file}_bass.wav")


def build_other(file, mode='upload'):
    directory = rf"{os.getcwd()}\songs\{file}"
    if mode == 'record':
        directory = rf"{os.getcwd()}\songs\{file}\user"
    wavio.write(rf"{directory}\{file}_other.wav", sources[2][0] + sources[2][1], sample_rate, sampwidth=2)
    sound = AudioSegment.from_wav(rf"{directory}\{file}_other.wav")
    sound.export(rf"{directory}\{file}_other.mp3", format='mp3')
    os.remove(rf"{directory}\{file}_other.wav")
    return rf"{directory}\{file}_other.mp3"


def build_vocal_drums(file, mode='upload'):
    directory = rf"{os.getcwd()}\songs\{file}"
    if mode == 'record':
        directory = rf"{os.getcwd()}\songs\{file}\user"
    vocal1 = sources[0][0] + sources[0][1]
    vocal2 = sources[3][0] + sources[3][1]
    wavio.write(rf"{directory}\{file}_vocal_drums.wav", vocal1 + vocal2, sample_rate, sampwidth=2)
    sound = AudioSegment.from_wav(rf"{directory}\{file}_vocal_drums.wav")
    sound.export(rf"{directory}\{file}_vocal_drums.mp3", format='mp3')
    os.remove(rf"{directory}\{file}_vocal_drums.wav")


def build_playback(file):
    directory = rf"{os.getcwd()}\songs\{file}"
    playback1 = sources[0][0] + sources[0][1]
    playback2 = sources[1][0] + sources[1][1]
    wavio.write(rf"{directory}\{file}_playback.wav", playback1 + playback2,
                sample_rate, sampwidth=2)
    sound = AudioSegment.from_wav(rf"{directory}\{file}_playback.wav")
    sound.export(rf"{directory}\{file}_playback.mp3", format='mp3')
    os.remove(rf"{directory}\{file}_playback.wav")


def build_song_without_guitar(file, mode='upload'):
    directory = rf"{os.getcwd()}\songs\{file}"
    if mode == 'record':
        directory = rf"{os.getcwd()}\songs\{file}\user"
    wavio.write(rf"{directory}\{file}_song_without_guitar.wav",
                sources[1][0] + sources[1][1] + sources[0][0] + sources[0][1] + sources[3][0] + sources[3][1],
                sample_rate, sampwidth=2)
    sound = AudioSegment.from_wav(rf"{directory}\{file}_song_without_guitar.wav")
    sound.export(rf"{directory}\{file}_song_without_guitar.mp3", format='mp3')
    os.remove(rf"{directory}\{file}_song_without_guitar.wav")

# The default set of pretrained weights that has been loaded has 4 sources that it is separated into: drums, bass, other, and vocals in that order. They have been stored into the dict “audios” and therefore can be accessed there. For the four sources, there is a separate cell for each, that will create the audio, the spectrogram graph, and also calculate the SDR score. SDR is the signal-to-distortion ratio, essentially a representation to the “quality” of an audio track.

# N_FFT = 4096
# N_HOP = 4
# stft = torchaudio.transforms.Spectrogram(
#     n_fft=N_FFT,
#     hop_length=N_HOP,
#     power=None,
# )
