import joblib
import pandas as pd
from more_functions import find_harmonics
import os

from more_functions import convert_to_wav

model = joblib.load('rfc_model.pkl')


def save_song_data(filename):
    data = []
    max_harm_length = 0
    freq_peaks = find_harmonics(filename)
    max_harm_length = max(max_harm_length, len(freq_peaks))
    cur_data = [filename]
    cur_data.extend([freq_peaks.min(), freq_peaks.max(), len(freq_peaks)])
    cur_data.extend(freq_peaks)
    data.append(cur_data)

    # Create columns for DataFrame
    cols = ["File Name", "Min Harmonic", "Max Harmonic", "# of Harmonics"]
    for i in range(max_harm_length):
        cols.append("Harmonic {}".format(i + 1))

    print(f"Length of cur_data: {len(cur_data)}")
    print(f"Number of columns: {len(cols)}")

    # Ensure the number of columns matches the data length
    if len(cur_data) != len(cols):
        raise ValueError("Number of columns does not match the data length")

    # Creating DataFrame
    df = pd.DataFrame(data, columns=cols)

    for i in range(1, 21):
        curr_interval = "Interval {}".format(i)
        curr_harm = "Harmonic {}".format(i + 1)
        prev_harm = "Harmonic {}".format(i)
        if curr_harm in df.columns and prev_harm in df.columns:
            df[curr_interval] = df[curr_harm].div(df[prev_harm], axis=0)

    for i in range(2, 14):
        curr_interval = "Interval {}_1".format(i)
        curr_harm = "Harmonic {}".format(i)
        if curr_harm in df.columns:
            df[curr_interval] = df[curr_harm].div(df["Harmonic 1"], axis=0)

    columns = ["Interval 1", "Interval 2", "Interval 3", "Interval 4"]
    columns.extend(["Interval 4_1", "Interval 5_1", "Interval 6_1"])
    try:
        res = df[columns]
    except KeyError as e:
        print(f"KeyError: {e}. Skipping prediction.")
        return None
    return res


def get_prediction(audio_file):
    wav_file = convert_to_wav(audio_file, output_dir=".")
    file_data = save_song_data(wav_file)
    print(file_data)
    try:
        prediction = model.predict(file_data.iloc[[0]])
        print("prediction:", prediction)
    except KeyError as e:
        print(f"KeyError: {e}. Skipping prediction.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}. Skipping prediction.")
        return None

    if prediction == 0:
        print("minor")
        return "Minor"
    print("major")
    return "Major"
