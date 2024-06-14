import React, { FC, useEffect, useState } from 'react';
import './RecordingCords.scss';
import fileService from '../../service/file.service';
import play from '../../assets/btn-play.png'
import bgUrl from '../../assets/pages-bg.png'

interface RecordingCordsProps { }

const RecordingCords: FC<RecordingCordsProps> = () => {
  const [currentIndex, setCurrentIndex] = useState<number>(-1);
  const [currentName, setCurrentName] = useState<string>('');
  const [chordsData, setChordsData] = useState<any>([]);
  const [audioUrl, setAudioUrl] = useState<string>('');

  useEffect(() => {
    getUserRecord();
    getUserChords();
  }, [])

  useEffect(() => {
    if (currentIndex >= 0) {
      if (currentIndex < chordsData.length) {
        const currentObject = chordsData[currentIndex];
        setCurrentName(currentObject[0].name);

        const timer = setTimeout(() => {
          setCurrentIndex((prevIndex) => prevIndex + 1);
        }, currentObject[0].seconds * 1000);

        // Cleanup the timer when component unmounts or index changes
        return () => clearTimeout(timer);
      }
    }

  }, [currentIndex]);

  const getUserChords = async () => {
    const d = await fileService.getUserChordsFile();
    setChordsData(d)
  }
  const getUserRecord = async () => {
    const url = await fileService.getUserRecording();
    setAudioUrl(url);
  }
  return (
    <div className='RecordingCords' style={{ backgroundImage: `url(${bgUrl})` }}>
      <h4>You can listen to your performance recording<br /> while viewing the identified chords.</h4>
      <img src={play} onClick={() => {
        document.getElementById('a')?.setAttribute('src', audioUrl);
        setCurrentIndex(0)
      }} alt="play audio" />
      <audio id='a' style={{ display: 'none' }} autoPlay></audio>
      <h1>{currentIndex} : {currentName}</h1>
    </div>)
}

export default RecordingCords;
