import React, { Suspense, useRef } from 'react';
import { useState } from "react";
import './App.scss';
import '../node_modules/bootstrap/';
// import { Route, Routes, useNavigate } from 'react-router-dom';
import Home from './components/Home/Home';
import Loader from './components/loading/loading';
import Try from './components/try/try';
import AudioProcessor from './components/AudioProcessor/AudioProcessor';
import AudioRecorder from './components/AudioRecorder/AudioRecorder';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import UploadFile from './components/UploadFile/UploadFile';


const App: React.FC = () => {
    return (
        <div >
            <Routes>
                <Route path='/' element={<UploadFile/>}></Route>
                <Route path='/record' element={<AudioRecorder />}></Route>
                {/* <Route path='compare' element={}></Route> */}
            </Routes>
            {/* <Try></Try> */}
            {/* <AudioRecorder /> */}
        </div>
    );
};

export default App;

//  https://css-loaders.com/colorful/#l9
//  css loading website
