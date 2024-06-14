import React, { useRef, useState } from 'react';
import './AudioRecorder.scss';
import { useLocation, useNavigate } from 'react-router-dom';
import bg from '../../assets/pages-bg.png'
import Loader from '../Loader/Loader';

const AudioRecorder: React.FC = () => {
  const [recordedUrl, setRecordedUrl] = useState<string>('');
  const mediaStream = useRef<MediaStream | null>(null);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  const [started, setStarted] = useState<boolean>(false)
  const [stopped, setStopped] = useState<boolean>(false)
  const [recordedBlob, setRecordedBlob] = useState<Blob>(new Blob());
  const navigate = useNavigate();
  const location = useLocation();
  const songToLoad = location.state
  const [isLoading, setIsLoading] = useState(false)

  const startRecording = async (): Promise<void> => {
    try {
      // Request access to the microphone with the desired sample rate
      const stream: MediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 44100,  // Set the desired sample rate
          echoCancellation: true,  // Optional: Enable echo cancellation
        },
      });

      mediaStream.current = stream;

      // Create a MediaRecorder instance
      mediaRecorder.current = new MediaRecorder(stream, {
        mimeType: 'audio/webm',  // You can also use 'audio/wav' or other supported formats
      });

      mediaRecorder.current.ondataavailable = (e: BlobEvent) => {
        if (e.data.size > 0) {
          chunks.current.push(e.data);
        }
      };

      mediaRecorder.current.onstop = () => {
        const recBlob: Blob = new Blob(chunks.current, { type: 'audio/webm' });
        setRecordedBlob(recBlob);
        const url: string = URL.createObjectURL(recBlob);
        setRecordedUrl(url);
        chunks.current = [];
      };

      mediaRecorder.current.start();
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = (): void => {
    if (mediaRecorder.current && mediaRecorder.current.state === 'recording') {
      mediaRecorder.current.stop();
    }
    if (mediaStream.current) {
      mediaStream.current.getTracks().forEach((track: MediaStreamTrack) => {
        track.stop();
      });
    }
  };

  const sendBlobToServer = async (blob: Blob): Promise<void> => {
    const formData = new FormData();
    formData.append('audio', blob, 'recording.webm');

    try {
      const response = await fetch('http://localhost:5000/upload_record', {
        method: 'POST',
        body: formData,
      });
      console.log(response)
      if (response.ok) {
        console.log('Blob sent successfully!');
        navigate('/feedback-option')
      } else {
        console.error('Failed to send blob');
      }
    } catch (error) {
      console.error('Error sending blob to server:', error);
    }
  };

  return (
    <div className='audio-recorder' style={{ backgroundImage: `url(${bg})` }}>
      <div className='content'>
        <h2>Record your perfomance---</h2>
        <h5>Here you can listen to {songToLoad} and play your guitar<br /> with it according listening.</h5>
        <audio controls>
          <source src={songToLoad} type="audio/wav"></source>
        </audio><br />
        {recordedUrl != '' ? <div><p>your recording ⬇️ </p><audio controls src={recordedUrl} /></div> : ""}

        {
          !started ? <i className="pi pi-microphone" onClick={() => { setStarted(true); startRecording() }} style={{ fontSize: '4rem' }}></i> :
            <i className={stopped ? "hide" : "pi pi-stop-circle"} style={{ fontSize: '4rem' }} onClick={() => { setStopped(true); stopRecording(); }}></i>
        }
        {
          stopped ? <div><button className='r' onClick={() => { setRecordedUrl(''); setStarted(false); setStopped(false) }}>Restart Recording</button>
            <button className='s' onClick={async () => {
              await sendBlobToServer(recordedBlob);
            }}>Send Record</button>
          </div> : ""
        }
        {isLoading ? <Loader></Loader> : ""}
      </div >
    </div>
  );
};

export default AudioRecorder;

