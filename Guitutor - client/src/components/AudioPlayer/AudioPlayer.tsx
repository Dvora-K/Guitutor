import React, { FC, useEffect, useState } from 'react';
import './AudioPlayer.scss';
import useSound from "use-sound"; // for handling the sound
import playbtn from '../../assets/btn-play.png'
import stop from '../../assets/btn-stop.png'
import fileService from '../../service/file.service';

interface AudioPlayerProps {
  song:any,
  width: any,
  height: any
}

const AudioPlayer: FC<AudioPlayerProps> = (props: AudioPlayerProps) => {
  const [isPlaying, setIsPlaying] = useState(false);
  // const [props.song, setprops.song] = useState<any>()
  const [play, { pause, duration, sound }] = useSound(props.song);

  useEffect(() => { console.log(typeof (props.song)); console.log(props.song) }, [])
  // useEffect(() => { getSourceFromServer() }, [])

  const getSourceFromServer = async () => {
    try {
      const url = await fileService.getSource('vocal_drums');
      // return url;
      // setprops.song(url)
    }
    catch (err) {
      console.error('Error fetching Audio:', err);
    }
  }
  const playingButton = () => {
    if (isPlaying) {
      pause(); // this will pause the audio
      setIsPlaying(false);
    } else {
      play(); // this will play the audio
      setIsPlaying(true);
    }
  };
  return (
    <div className="component">
      <div>
        {!isPlaying ? (
          <button style={{ backgroundImage: `url(${playbtn})`, width: props.width, height: props.height }} onClick={playingButton}></button>
        ) : (
          <button style={{ backgroundImage: `url(${stop})`, width: props.width, height: props.height }} onClick={playingButton}></button>
        )}
      </div>
    </div>
  );
}

export default AudioPlayer;
