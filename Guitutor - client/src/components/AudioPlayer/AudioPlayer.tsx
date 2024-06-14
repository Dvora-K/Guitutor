import React, { FC, useState } from 'react';
import './AudioPlayer.scss';
import useSound from "use-sound"; // for handling the sound
import playbtn from '../../assets/btn-play.png'
import stop from '../../assets/btn-stop.png'

interface AudioPlayerProps {
  song: any,
  width: any,
  height: any
}

const AudioPlayer: FC<AudioPlayerProps> = (props: AudioPlayerProps) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [play, { pause, duration, sound }] = useSound(props.song);
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
