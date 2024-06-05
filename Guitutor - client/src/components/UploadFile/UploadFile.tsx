import React, { FC, useEffect, useRef, useState } from 'react';
import { UploadOutlined } from '@ant-design/icons';
import { Button, Upload } from 'antd';
import './UploadFile.scss';
import { useNavigate } from 'react-router-dom';
import FileService from '../../service/file.service';
import { Message } from 'primereact/message';
import Loading from '../loading/loading';
import fileService from '../../service/file.service';
interface UploadFileProps { }

const UploadFile: FC<UploadFileProps> = () => {
  const [uploadedFile, setUploadedFile] = useState<any>([]);
  const [vocalUrl, setVocalUrl] = useState<any>('');
  const [playbackUrl, setPlaybackUrl] = useState<any>('');
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
      setIsLoading(false); // Set isLoading to false after the request finishes
    } catch (err) {
      throw err;
    }
  }

  const getVocal = () => {
    const vocal = getSourceFromServer('vocal');
    setVocalUrl(vocal)
  };

  const getPlayback = () => {
    const playback = getSourceFromServer('playback');
    setPlaybackUrl(playback)
  }
  const getSongWithoutGuitar = () => {
    const song = getSourceFromServer('song_without_guitar');
    setSongWithoutGuitar(song)
  };

  const getSourceFromServer = async (req: string) => {
    try {
      const url: string = await FileService.getSource(req);
      setChoice(url);
      return url;
    }
    catch (err) {
      console.error('Error fetching Audio:', err);
    }
  }

  return <div className="UploadFile">
    <input style={{ display: 'none' }} ref={uploadInputRef} type='file' onChange={selectedFile} ></input>
    {
      uploadedFile == '' ? <div>
        <div className='select' onDragOver={(event) => { event.preventDefault() }} >
          <Button style={{ backgroundColor: '#0041d8', color: '#fff' }} onClick={() => { uploadInputRef.current.click() }} icon={<UploadOutlined />}>Select Song</Button></div>
        {errorMessage && <Message severity="error" text={errorMessage} />}</div>
        : <div className='upload-list'>{uploadedFile[0].name}</div>
    }

    {
      isLoading ? <Loading></Loading> : ""
    }

    {
      !isLoading && typeof uploadedFile[0] != "undefined" ?
        <div> {/* define buttons from the server response*/}
          <p>Try Join Guitar To---</p><br></br>
          <button onClick={() => getVocal()}>Vocal and Drums (for the rate:)</button>
          <button onClick={() => getPlayback()}>Playback (without guitar ofcourse:)</button>
          <button onClick={() => getSongWithoutGuitar()}>Playback + Vocal</button><br /><br />
          <button onClick={() => navigate('/record', { state: choice })}>Let's Start Record Together</button>
        </div> : ""
    }
    {
      choice!=''?<audio src={choice} controls></audio>:''
    }
    {/*  איך לעשות שהשיר יושמע ללא הרצועת שמע הדיפולטיבית אלא ע"י כפתור אחר?*/}
  </div >
}

export default UploadFile;
