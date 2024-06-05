// import React, { FC, forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
// import { UploadOutlined } from '@ant-design/icons';
// import { Button, Upload } from 'antd';
// // import type { UploadFile } from 'antd';
// import { Message } from 'primereact/message';
// import FilesService from '../../service/file.service'
// import './try.scss'
// import '../loading/loading'
// import Loading from '../loading/loading';
// import { Navigate, useNavigate } from 'react-router-dom';
// interface tryProps { }

const Try = () => {

  //   const [songFile, setSongFile] = useState<any>([]);
  //   // const [pdfUrl, setPdfUrl] = useState<any>([]);
  //   const [vocalUrl, setVocalUrl] = useState<any>('');
  //   const [playbackUrl, setPlaybackUrl] = useState<any>('');
  //   const [songWithoutGuitarUrl, setSongWithoutGuitar] = useState<any>('');
  //   const [isLoading, setIsLoading] = useState<boolean>(false)
  //   const [errorMessage, setErrorMessage] = useState('');
  //   const navigate = useNavigate();

  //   const uploadInputRef = useRef<any>();

  //   useEffect(() => {
  //     console.log("השתנה")
  //     console.log(songFile)
  //     let s = typeof songFile[0]
  //     console.log(typeof s)
  //     if (songFile != '')
  //       sendFile();
  //   }, [songFile])

  //   const convertsongFileToArr = (songFile: FileList): [] => {
  //     let array: any = [];
  //     array.push(songFile.item(0))
  //     return array;
  //   }

  //   const selectedFile = (event: any) => {
  //     let file: FileList = event.target.files;
  //     if (file.item(0)?.type == 'audio/mpeg') {
  //       let arr = convertsongFileToArr(file);
  //       setSongFile([...arr])
  //     }
  //     else {
  //       setErrorMessage('It is not possible to load a file of this type.');
  //     }
  //   };

  //   const sendFile = async () => {
  //     setIsLoading(true);
  //     try {
  //       await FilesService.send(songFile);
  //       setIsLoading(false); // Set isLoading to false after the request finishes
  //     } catch (err) {
  //       throw err;
  //     }
  //   }

  //   // const getPdf = () => {
  //   //   FilesService.getPdf()
  //   //     .then(url => {
  //   //       setPdfUrl(url);
  //   //     })
  //   //     .catch(error => {
  //   //       console.error('Error fetching PDF:', error);
  //   //     });
  //   // };

  //   const getVocal = () => {
  //     FilesService.getVocal()
  //       .then(url => {
  //         setVocalUrl(url);
  //       })
  //       .catch(error => {
  //         console.error('Error fetching Audio:', error);
  //       });
  //   };

  return <div className='area'></div>
}
{/* //     <input style={{ display: 'none' }} ref={uploadInputRef} type='file' onChange={selectedFile} multiple></input>
//     {songFile == '' ? <div>
//       <br />
//       <div className='select' onDragOver={(event) => { event.preventDefault() }} ><Button style={{ backgroundColor: '#0041d8', color: '#fff' }} onClick={() => { uploadInputRef.current.click() }} icon={<UploadOutlined />}>Select File</Button></div>
//       {errorMessage && <Message severity="error" text={errorMessage} />}
//       <br /></div> : <div><h5>file selcted:</h5>
//       {songFile.map((f: any) => <div className='upload-list'>{f.name}</div>)}</div>}
//     <br />

//     {isLoading ? <Loading></Loading>
//       : <button onClick={() => navigate('/record')}>Let's Record Together</button>}
//     {
//       typeof songFile[0] != "undefined"
//         && !isLoading ? <div className='row'><button className='btn btn-primary col-sm-3' onClick={() => { }}>get pdf of notes</button><button className='btn btn-primary col-sm-3' onClick={getVocal}>get vocal</button>
//         <br /><button className='btn btn-primary col-sm-3' onClick={() => setSongFile([])}>choose another file</button></div>
//         : ''}

//     {/* {pdfUrl !== '' ?
//       <iframe
//         src={pdfUrl}
//         title="PDF Viewer"
//         style={{ width: '100%', height: '600px' }}
//       /> : ''
//     } */}
//     <br />
//     <div>
//       {vocalUrl != '' ?
//         <div>
//           <audio controls>
//             <source src={vocalUrl} type="audio/wav"></source>
//           </audio></div> : ''
//       }
//     </div>
//     <canvas></canvas>
//   </div>
// } */}
export default Try;


// // מעוצבת -הכל
// //   const songFile: UploadFile[] = [];
// //   console.log(songFile)

// //   return <div className="UpLoadFiles">
// //     <br />
// //     <Upload
// //       action="https://run.mocky.io/v3/435e224c-44fb-4773-9faf-380c5e6a2188"
// //       listType="picture"
// //       defaultsongFile={[...songFile]}
// //       className="upload-list-inline"
// //     >
// //       <Button icon={<UploadOutlined />}>Upload</Button>
// //     </Upload>
// //   </div>
// // })