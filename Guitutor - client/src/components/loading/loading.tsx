import React, { FC } from 'react';
import './loading.scss';

interface LoadingProps {
}

const Loading: FC<LoadingProps> = () => (
  <div className='loader-container col-sm-6'>
    <div className='my-loadder'>
      <div className="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
    </div>
    <span className='col-sm-6'>מעבד</span>
  </div>
  // <div className="Loading"> 
  //   <div className="loader"></div>
  // </div>
);

export default Loading;
