import React, { Suspense, useRef } from 'react';
import './App.scss';
import '../node_modules/bootstrap/';
import HomePage from './components/HomePage/HomePage';
import AudioRecorder from './components/AudioRecorder/AudioRecorder';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import UploadFile from './components/UploadFile/UploadFile';
import FileComparison from './components/FileComparison/FileComparison';
import Loader from './components/Loader/Loader';
import AudioPlayer from './components/AudioPlayer/AudioPlayer';
import Try from './components/try/try'
import RecordingCords from './components/RecordingCords/RecordingCords';
import FeedbackOptions from './components/FeedbackOptions/FeedbackOptions';
import qala from './assets/song.mp3' // importing the music


const App: React.FC = () => {
    return (
        <div className='App'>
            <Routes>
                <Route path='aa' element={<AudioPlayer song={qala} width={'100px'} height={'100px'} />}></Route>
                <Route path='/' element={<HomePage></HomePage>}></Route>
                <Route path='/upload-file' element={<UploadFile />}></Route>
                <Route path='/user-record' element={<AudioRecorder />}></Route>
                <Route path='feedback-option' element={<FeedbackOptions />}></Route>
                <Route path='compare-chords' element={<FileComparison />}></Route>
                <Route path='play-user-recording' element={<RecordingCords />}></Route>
            </Routes>
        </div>
    );
};

export default App;

//  https://css-loaders.com/colorful/#l9
//  css loading website
