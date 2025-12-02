import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import myVideo from "../../french_final.mp4";

function App() {

  return (
    <div className="page">
      <div className="videoContainer">
        <video
          src={myVideo}
          controls
          className="vid"
        />
      </div>
      <div className="rightContent">
        <div className="tts">
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu facilisis dui, in efficitur tellus. Curabitur eu turpis nec ipsum fermentum imperdiet at et tellus. Cras varius eu lectus id semper. Sed vel felis eget ipsum aliquam consectetur a ut mauris. Vestibulum erat mi, varius in est ut, pharetra mattis dolor. Quisque quis bibendum erat, id consectetur mi. Maecenas ullamcorper metus sit amet magna scelerisque, non convallis lacus sagittis.Ut consectetur et augue et condimentum. Quisque efhruilgriesuzgliuflskjfnlgkzsjbglkjzsblgjzs zlsjdglskjgblkjszbdg</p>
        </div>
        <div className="lessonContainer">
          Lesson container
        </div>
      </div>
    </div>
  )
}

export default App
