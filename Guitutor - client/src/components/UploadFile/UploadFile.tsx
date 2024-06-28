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
import s from '../../assets/song.mp3'
import fileService from '../../service/file.service';
import { url } from 'inspector';
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
    console.log("choice:", choice)
  }, [choice])

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

  const dropFile = (e: any) => {
    e.preventDefault();
    let files = e.dataTransfer.files;
    const file = files.item(0);
    if (file?.type == 'audio/mpeg' || file?.type == 'audio/wav') {
      let arr = convertFileListToArr(files);
      setUploadedFile([...arr])
    }
    else {
      setErrorMessage('It is not possible to load a file of this type.');
    }
  }

  const sendFile = async () => {
    setIsLoading(true);
    try {
      await FileService.send(uploadedFile);
      // await getVocalDrums();
      // await getTune()
      // await getSongWithoutGuitar();
      setIsLoading(false); // Set isLoading to false after the request finishes
    } catch (err) {
      throw err;
    }
  }

  const getVocalDrums = async () => {
    const vocal = await getSourceFromServer('vocal_drums');
    setVocalDrumsUrl(vocal)
    setChoice(vocal)
    console.log("VocalDrumsUrl", vocal)
  };

  const getTune = async () => {
    const tune = await getSourceFromServer('tune');
    setTune(tune)
    setChoice(tune)
    console.log("tuneUrl", tune)
  }
  const getSongWithoutGuitar = async () => {
    const song = await getSourceFromServer('song_without_guitar');
    setSongWithoutGuitar(song)
    setChoice(song)
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
          <div onDrop={dropFile} onDragOver={(event) => { event.preventDefault() }} >
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
              <div className='vocalDrumsOption'>
                {/* <AudioPlayer song={s} width={'80px'} height={'80px'} /> */}
                <button onClick={async () => await getVocalDrums()}> Vocal + Drums </button>
                {/* <p>Vocal + Drums</p> */}
              </div>
              <div className='tuneOption'>
                {/* <AudioPlayer song={tuneUrl} width={'80px'} height={'80px'} /> */}
                <button onClick={getTune}> Tune </button>
                {/* <p>Tune</p> */}
              </div>
              <div className='songOption'>
                <button onClick={getSongWithoutGuitar}> Song without guitar </button>
                {/* <AudioPlayer song={songWithoutGuitarUrl} width={'80px'} height={'80px'} /> */}
                {/* <p>Song without guitar</p> */}
              </div>
            </div>
            {
              choice != '' ? <audio controls> <source src={choice} /></audio> : ''
            }
            <br />
            <img style={{ marginLeft: '18%', cursor: 'pointer' }} src={record} onClick={() => navigate('/user-record', { state: choice })}></img>
          </div>
          : ""
      }

    </div >
  </div>

}

export default UploadFile;
