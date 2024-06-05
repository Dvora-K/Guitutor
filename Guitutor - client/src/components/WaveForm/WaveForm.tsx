import React, { FC, useEffect, useRef } from 'react';
import './WaveForm.scss';
// import waveformData from './waveform_data.json';

interface WaveFormProps {
  data:any
}

const WaveForm: FC<WaveFormProps> = (props:WaveFormProps) =>{
  const canvasRef = useRef(null);

useEffect(() => {
  // const canvas = canvasRef.current;
  // const ctx = canvas?.getContext('2d');
  // const {width, height} :any = canvas;
  // const middleY = height / 2;
  // ctx.clearRect(0, 0, width, height);
  // ctx.beginPath();

  // props.data.forEach((point:any, i:any) => {
  //   const x = (i / props.data.length) * width;
  //   const y = middleY - point * middleY;
  //   ctx.lineTo(x, y);
  // });

  // ctx.strokeStyle = '#FFCC00'; // Set the line color
  // ctx.lineWidth = 2;
  // ctx.stroke();
}, [props.data]);

return (
  <canvas
    ref={canvasRef}
    width="600" // Set the canvas width
    height="100" // Set the canvas height
  />
);
};


export default WaveForm;
