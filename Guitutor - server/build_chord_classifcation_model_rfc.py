import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from recognize_chord_name import find_harmonics


def build_model(path):
    # build model
    data = []
    # 278, 55.0
    max_harm_length = 0  # i will keep track of max harmonic length for naming columns

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

    # Column Names for DataFrame:
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

    # Preprocessing Data
    df["Chord Type"] = df["Chord Type"].replace("Major", 1)
    df["Chord Type"] = df["Chord Type"].replace("Minor", 0)
    # df.to_csv('Training.csv', index=False)

    columns = ["Interval 1", "Interval 2", "Interval 3", "Interval 4"]
    columns.extend(["Interval 4_1", "Interval 5_1", "Interval 6_1"])
    train_X, val_X, train_y, val_y = train_test_split(df[columns], df["Chord Type"], test_size=0.40, random_state=0)
    train_X.head()
    training = train_X.copy()
    training['Target'] = train_y
    training.to_csv('Training.csv', index=False)

    # Model Building
    rfc = RandomForestClassifier(random_state=0)
    score_rfc = cross_val_score(rfc, train_X, train_y, cv=10).mean()
    print("Cross Val Score for Random Forest Classifier: {:.2f}".format(score_rfc))
    # defining my classifier
    classifier = RandomForestClassifier(random_state=0)

    classifier.fit(train_X, train_y)  # training classifier
    pred_y = classifier.predict(val_X)  # making prediction on validation
    cm = confusion_matrix(val_y, pred_y)
    acc = accuracy_score(val_y, pred_y)

    print("Confusion Matrix:")
    print(cm)
    print("Accuracy Score: {:.2f}".format(acc))
    rfc.fit(train_X, train_y)

    # Save the trained model to a file
    import joblib
    joblib.dump(rfc, 'rfc_model.pkl')


if __name__ == "__main__":
    build_model(r"C:\Users\User\Desktop\פרויקט בינה מלאכותית 20.5.24\Audio_Files")
