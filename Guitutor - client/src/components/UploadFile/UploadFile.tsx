import React, { FC, useEffect, useRef, useState } from 'react';
import './UploadFile.scss';
import { useNavigate } from 'react-router-dom';
import FileService from '../../service/file.service';
import { Message } from 'primereact/message';
import blogoImg from '../../assets/logo-black.png'
import bgUrl from '../../assets/pages-bg.png'
import record from '../../assets/btn-record.png'
import Loader from '../Loader/Loader';
import AudioPlayer from '../AudioPlayer/AudioPlayer';

interface UploadFileProps { }

const UploadFile: FC<UploadFileProps> = () => {
  const [uploadedFile, setUploadedFile] = useState<any>([]);
  const [vocalDrumsUrl, setVocalDrumsUrl] = useState<any>('');
  const [tuneUrl, setTune] = useState<any>('');
  const [songWithoutGuitarUrl, setSongWithoutGuitar] = useState<any>('');
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [errorMessage, setErrorMessage] = useState('');
  const [choice, setChoice] = useState<any>('');

  const uploadInputRef = useRef<any>();
  const navigate = useNavigate();

  useEffect(() => {
    if (uploadedFile != '')
      sendFile();
  }, [uploadedFile])

  const convertFileListToArr = (songFile: FileList): [] => {
    let array: any = [];
    array.push(songFile.item(0))
    return array;
  }

  const selectedFile = (event: any) => {
    let files: FileList = event.target.files;
    const file = files.item(0);
    if (file?.type == 'audio/mpeg' || file?.type == 'audio/wav') {
      let arr = convertFileListToArr(files);
      setUploadedFile([...arr])
    }
    else {
      setErrorMessage('It is not possible to load a file of this type.');
    }
  };

  const sendFile = async () => {
    setIsLoading(true);
    try {
      await FileService.send(uploadedFile);
      getVocalDrums();
      getTune()
      getSongWithoutGuitar();
      setIsLoading(false); // Set isLoading to false after the request finishes
    } catch (err) {
      throw err;
    }
  }

  const getVocalDrums = async () => {
    const vocal = await getSourceFromServer('vocal_drums');
    setVocalDrumsUrl(vocal)
    console.log("VocalDrumsUrl", vocal)
  };

  const getTune = async () => {
    const tune = await getSourceFromServer('tune');
    setTune(tune)
    console.log("tuneUrl", tune)
  }
  const getSongWithoutGuitar = async () => {
    const song = await getSourceFromServer('song_without_guitar');
    setSongWithoutGuitar(song)
  };

  const getSourceFromServer = async (req: string) => {
    try {
      const url = await FileService.getSource(req);
      return url;
    }
    catch (err) {
      console.error('Error fetching Audio:', err);
    }
  }

  return <div className="UploadFile" style={{ backgroundImage: `url(${bgUrl})` }} >
    <img src={blogoImg}></img>
    <div className='cont'>
      <input style={{ display: 'none' }} ref={uploadInputRef} type='file' onChange={selectedFile} ></input>
      {
        uploadedFile == '' ? <div>
          <div onDragOver={(event) => { event.preventDefault() }} >
            <div className='select-area' onDrag={() => { }} onClick={() => { uploadInputRef.current.click() }}>Drag or Select a Song<br />(only format wav/mp3)</div>
            {errorMessage && <Message severity="error" text={errorMessage} />}</div>
        </div> :
          <div className='upload-list'> {uploadedFile[0].name}</div>
      }

      {
        isLoading ? <Loader></Loader> : ""
      }

      {
        !isLoading && typeof uploadedFile[0] != "undefined" ?
          <div> {/* define buttons from the server response*/}
            <h5> Choose what to accompany your guitar playing---</h5><br></br>
            <div className='sources-options'>
              <div onClick={() => setChoice(vocalDrumsUrl)} className='option'>
                <AudioPlayer song={vocalDrumsUrl} width={'80px'} height={'80px'} />
                <audio ><source src='http://localhost:5000/get_vocal_drums' /></audio>
                <p>Vocal + Drums</p>
              </div>
              <div className='option'>
                <AudioPlayer song={tuneUrl} width={'80px'} height={'80px'} />
                <audio controls><source type='audio/mpeg' src='http://localhost:5000/get_tune'></source></audio>
                <p>Tune</p>
              </div>
              <div onClick={() => setChoice(songWithoutGuitarUrl)} className='option'>
                <AudioPlayer song={songWithoutGuitarUrl} width={'80px'} height={'80px'} />
                <audio src='http://localhost:5000/get_song_without_guitar'></audio>
                <p>Song without guitar</p>
              </div>
            </div>
            <img style={{ marginLeft: '33%', cursor: 'pointer' }} src={record} onClick={() => navigate('/user-record', { state: choice })}></img>
          </div>
          : ""
      }
      {
        choice != '' ? <audio style={{ display: 'none' }} autoPlay src={choice} ></audio> : ''
      }
      {/*  איך לעשות שהשיר יושמע ללא הרצועת שמע הדיפולטיבית אלא ע"י כפתור אחר?*/}
    </div >
  </div>

}

export default UploadFile;
