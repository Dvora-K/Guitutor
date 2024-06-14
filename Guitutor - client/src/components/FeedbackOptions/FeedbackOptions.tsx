import React, { FC } from 'react';
import './FeedbackOptions.scss';
import { useNavigate } from 'react-router-dom';
import bg from '../../assets/pages-bg.png'
interface FeedbackOptionsProps { }

const FeedbackOptions: FC<FeedbackOptionsProps> = () => {

  const navigate = useNavigate()

  return <div className="FeedbackOptions" style={{ backgroundImage: `url(${bg})` }}>
    <h3>Your recording has been saved and analyzed by us. <br /><br />
      Choose a way in which you would like to receive feedback on your performance ---</h3><br />
    <div><button className='c' onClick={() => navigate('/compare-chords')}> Compare your chords </button>
      <button className='p' onClick={() => navigate('/play-user-recording')}> Listening & Get your chords </button>
    </div></div>
}

export default FeedbackOptions;
