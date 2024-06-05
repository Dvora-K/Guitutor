from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import os
import joblib

from recognize_chord_name import find_harmonics

def build_model(path):
    # Build model
    data = []
    max_harm_length = 0  # Track max harmonic length for naming columns

    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            foldername = os.path.basename(dirname)
            full_path = os.path.join(dirname, filename)
            freq_peaks = find_harmonics(full_path)
            max_harm_length = max(max_harm_length, len(freq_peaks))
            cur_data = [foldername, filename]
            cur_data.extend([freq_peaks.min(), freq_peaks.max(), len(freq_peaks)])
            cur_data.extend(freq_peaks)
            data.append(cur_data)

    # Column names for DataFrame
    cols = ["Chord Type", "File Name", "Min Harmonic", "Max Harmonic", "# of Harmonics"]

    for i in range(max_harm_length):
        cols.append("Harmonic {}".format(i + 1))

    # Creating DataFrame
    df = pd.DataFrame(data, columns=cols)

    for i in range(1, 21):
        curr_interval = "Interval {}".format(i)
        curr_harm = "Harmonic {}".format(i + 1)
        prev_harm = "Harmonic {}".format(i)
        df[curr_interval] = df[curr_harm].div(df[prev_harm], axis=0)

    for i in range(2, 14):
        curr_interval = "Interval {}_1".format(i)
        curr_harm = "Harmonic {}".format(i)
        df[curr_interval] = df[curr_harm].div(df["Harmonic 1"], axis=0)

    print(df)

    # Preprocessing data
    df["Chord Type"] = df["Chord Type"].replace("Major", 1)
    df["Chord Type"] = df["Chord Type"].replace("Minor", 0)

    # Columns used for training
    columns = ["Interval 1", "Interval 2", "Interval 3", "Interval 4"]
    columns.extend(["Interval 4_1", "Interval 5_1", "Interval 6_1"])

    # Splitting the data
    train_X, val_X, train_y, val_y = train_test_split(df[columns], df["Chord Type"], test_size=0.40, random_state=0)

    print(f"Total samples: {len(df)}")
    print(f"Training samples: {len(train_X)}")
    print(f"Validation samples: {len(val_X)}")

    # Model Building
    rfc = RandomForestClassifier(random_state=0)
    score_rfc = cross_val_score(rfc, train_X, train_y, cv=10).mean()
    print("Cross Val Score for Random Forest Classifier: {:.2f}".format(score_rfc))

    # Defining and training classifier
    classifier = RandomForestClassifier(random_state=0)
    classifier.fit(train_X, train_y)  # Training classifier
    pred_y = classifier.predict(val_X)  # Making prediction on validation
    cm = confusion_matrix(val_y, pred_y)
    acc = accuracy_score(val_y, pred_y)

    print("Confusion Matrix:")
    print(cm)
    print("Accuracy Score: {:.2f}".format(acc))

    # Save the trained model to a file
    joblib.dump(rfc, 'rfc_model.pkl')

if __name__ == "__main__":
    build_model(r"C:\Users\User\Desktop\פרויקט בינה מלאכותית 20.5.24\Audio_Files")
