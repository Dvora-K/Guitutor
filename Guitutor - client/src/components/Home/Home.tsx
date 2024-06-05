import React, { FC, useRef, useState } from 'react';
import './Home.scss';
// import UploadSong from '../UploadSong/UploadSong';
// import { FileUpload } from 'primereact/fileupload';
// import { Tooltip } from 'primereact/tooltip';
// import { Toast } from 'primereact/toast';

interface HomeProps { }

const Home: FC<HomeProps> = () => {

  const [songFile,setSongFile] = useState<any>([]);

  const [chordsFile,setChordsFile] = useState<any>();

  const [vocalFile,setVocalFile] = useState<any>();

  

  return <></>

}

export default Home;
