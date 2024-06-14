import React, { FC, useEffect } from 'react';
import './Loader.scss';
import loader from '../../assets/loader_gif.gif'
interface LoaderProps { }

const Loader: FC<LoaderProps> = () => {

  return <div> 
  <img src={loader} alt="Loading..." />
  </div >
}

export default Loader;
