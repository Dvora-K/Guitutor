## **Guitutor** - Real-Time Performance Feedback
Welcome to Guitutor - Guitar Learning System!
This project is designed to help beginners learn guitar by providing real-time feedback on their performance. The system allows users to select a song, which is processed and broken down into its musical components using a Convolutional Neural Network (CNN) model. Users can then play along with the deconstructed song, and their performance is analyzed using an AI classification model (Random Forest Classifier - RFC) and music-based algorithms to identify the chords played. The system compares these chords to the original song and returns feedback on the user's performance.

## Features
- **Song Selection**: Users can select a song to practice.
- **Real-Time Feedback**: Provides real-time feedback on user performance.
- **Chord Analysis**: Identifies chords played by the user and compares them to the original song.
- **Performance Analysis:** Analyzes user performance using an AI classification model.
- **User-Friendly Interface:** Easy-to-use interface for beginners.

## Usage

1. **Upload an Audio File:**
    Users upload an audio file of the song they want to practice.
2. **Analyze and Save Data:**
    The system processes the file, breaking it down into its musical components and saving the data on the server.
3. **Play Along:**
    Users play along with the deconstructed song.
4. **Record and Upload Performance:**
    The system records the user's performance and uploads it for analysis.
5. **Receive Feedback:**
    The system analyzes the performance, identifies the chords played, compares them to the original song, and provides feedback.

## Installation
1. **Clone Repository:**
     ```
     git clone https://github.com/Dvora-K/Guitutor.git
2. **Navigate to**`Guitutor`
3.  **Run in Docker platform**
    ```sh
      docker-compose build
      docker-compose up
    ```

## Technologies Used
- Server-Side:
   - Python (Flask) 
   - **Libraries and Tools**:
     - librosa, torch_audio, wavio, Pydub, Scipy
     - CNN and RFC Model
- Client-Side:
    React, TypeScript, SCSS
