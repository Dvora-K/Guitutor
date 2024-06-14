import React, { FC, useRef, useState } from 'react';
import './HomePage.scss';
// import logoImg from '../../assets/Guitutor-logo.jpg';
import { useNavigate } from 'react-router-dom';
import bg from '../../assets/gg.png'
import logo from '../../assets/wlogo.png'
interface HomePageProps { }

const HomePage: FC<HomePageProps> = () => {
  const navigate = useNavigate();
  return <div className='HomePage' >
    <div className='content'>
      <div className='bg' style={{ backgroundImage: `url(${bg})` }}><img src={logo} className='logo'></img></div>

      <div className='tt'>
        <h1> WEL<br/>COME :)</h1>
        {/* <img className='logo' src={lg}></img> */}
        <div className='text'> <h4>You dreamed of chords for songs you like,
          <br /> you wanted to accompany your favorite singers,
          <br /> you wanted to get feedback on playing by ear,
          <br /> all your dreams in one place --- </h4><br/>
          <h4> On this site you can have fun playing <br />
            any song you want on your guitar and <br />
            get feedback on your performance</h4>
          <button className='start' onClick={() => navigate('/upload-file')} >start</button></div>

        {/* <img className='logo' src={logoImg} alt="Guitutor-logo" /> */}
      </div>
    </div></div>

}

export default HomePage;
