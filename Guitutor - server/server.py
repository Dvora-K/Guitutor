from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import tempfile
from pydub import AudioSegment
import ast
import subprocess
# import our python files: #
import split_to_sources
from cut_song_to_sections import cut_song
from more_functions import makedir
from split_by_drums import split_by_drums_and_recognize_chords

# from recognize_chord_name import get_chords_of_song

os.environ["FFPROBE_PATH"] = r"C:\ffmpeg\bin\ffprobe.exe"

app = Flask(__name__)


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('song_file')
        print(files)
        if files:
            file = files[0]
            audio_data = file.read()
            fname = file.filename.split(".")
            global name
            name = fname[0]
            format_file = fname[1]
            # save the audio file # 
            with tempfile.NamedTemporaryFile(delete=False, suffix=format_file) as tmp_file:
                tmp_file.write(audio_data)
                tmp_filename = tmp_file.name

            print("accept and save file :" + name + " " + format_file)

            audio = AudioSegment.from_file(tmp_filename)

            # create folders according to song name to save all the song files #
            router_song_dir = rf"{os.getcwd()}\songs"
            output_folder = rf"{router_song_dir}\{name}"

            # # אם יש קבצים שקיימים למחוק אותם- אין צורך לשמור אותם
            # if os.path.exists(router_song_dir):
            #     os.unlink(router_song_dir)

            makedir(router_song_dir)
            makedir(output_folder)

            # save song in matching folder #
            audio.export(rf"{output_folder}\{name}.{format_file}", format="mp3")
            os.unlink(tmp_filename)
            print("Delete the temporary file")

            song_path = rf"{output_folder}\{name}.{format_file}"
            # split to sources #
            split_to_sources.load_song(song_path)
            split_to_sources.build_vocal_drums(name)
            # split_to_sources.build_song_without_guitar(name)
            split_to_sources.build_tune(name)
            path_drums = split_to_sources.build_drums(name)

            # subprocess.check_call([
            #     'lala_command.bat',
            #     song_path,
            #     output_folder
            # ])

            path_guitar = rf"{output_folder}\{name}_acoustic_guitar_split_by_lalalai.mp3"

            # split by drums rate #
            global song_chords_path
            song_chords_path = split_by_drums_and_recognize_chords(path_drums, path_guitar, name)

            os.remove(song_path)

            return jsonify({'succes': 200})
        return jsonify({'No file uploaded': 'not-ok'})


@app.route('/upload_record', methods=['POST'])
def upload_record():
    if 'audio' not in request.files:
        return "No file part", 400

    file = request.files['audio']
    if file.filename == '':
        return "No selected file", 400
    dir = rf'{os.getcwd()}\songs\{name}\user'
    makedir(dir)
    # Save the webm file
    webm_path = os.path.join(dir, f'rec_{name}.webm')

    file.save(webm_path)
    # Convert to wav
    wav_path = os.path.join(dir, f'rec_{name}.wav')
    audio = AudioSegment.from_file(webm_path, format='webm')
    audio.export(wav_path, format='wav')
    # convert to mp3
    mp3_path = os.path.join(dir, f'rec_{name}.mp3')
    audio.export(mp3_path, format='mp3')
    os.remove(webm_path)
    os.remove(wav_path)
    print(f"record were accepted and saved in {mp3_path}")

    split_to_sources.load_song(mp3_path)
    user_guitar = split_to_sources.build_other(name, 'record')
    user_drums = split_to_sources.build_drums(name, 'record')

    global user_chords_path
    user_chords_path = split_by_drums_and_recognize_chords(user_drums, user_guitar, name)

    return jsonify({200: 'ok'})


@app.route('/get_vocal_drums', methods=['GET'])
def return_vocal_drums():
    try:
        return send_file(rf"{os.getcwd()}\songs\{name}\{name}_vocal_drums.mp3")
    except Exception as e:
        return str(e)


@app.route('/get_tune', methods=['GET'])
def return_tune():
    try:
        return send_file(rf"{os.getcwd()}\songs\{name}\{name}_tune.mp3")
    except Exception as e:
        return str(e)


@app.route('/get_song_without_guitar', methods=['GET'])
def return_song_without_guitar():
    try:
        return send_file(rf"{os.getcwd()}\songs\{name}\{name}_no_acoustic_guitar_split_by_lalalai.mp3")
    except Exception as e:
        return str(e)


@app.route('/get_chords_files', methods=['GET'])
def get_chords():
    try:
        with open(song_chords_path, 'r', encoding='utf-8') as song:
            song_chords = song.read()
        with open(user_chords_path, 'r', encoding='utf-8') as user:
            user_chords = user.read()
        return {'song_chords': song_chords, 'user_chords': user_chords}
    except Exception as err:
        return str(err)


@app.route('/get_segment', methods=['GET'])
def get_seg():
    i = request.args.get('index')
    print(i)
    return send_file(rf'{os.getcwd()}\songs\{name}\segments\{i}.wav')


@app.route('/count_segments', methods=['GET'])
def count_seg():
    directory = rf'{os.getcwd()}\songs\{name}\segments'
    num_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    return jsonify({'num': num_files})


@app.route('/get_user_chords', methods=['GET'])
def get_user_chords():
    arr = []
    # Open the file and read line by line
    with open(user_chords_path, 'r') as file:
        for line in file:
            # Parse the line as a dictionary using ast.literal_eval
            line_dict = ast.literal_eval(line.strip())
            # Append the dictionary to the array
            arr.append(line_dict)
    return arr


@app.route('/get_user_rec', methods=['GET'])
def return_recording():
    try:
        return send_file(rf"{os.getcwd()}\songs\{name}\user\rec_{name}.mp3")
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    CORS(app)
    app.run()
