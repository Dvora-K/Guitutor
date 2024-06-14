import React, { useEffect, useState } from 'react';
import './FileComparison.scss';
import fileService from '../../service/file.service';
import { diffWords } from 'diff';
import bg from '../../assets/pages-bg.png'
const FileComparison: React.FC = () => {
  const [userChords, setUserChords] = useState<string | null>(null);
  const [songChords, setSongChords] = useState<string | null>(null);

  useEffect(() => {
    getFiles()
  }, []);

  const getFiles = async () => {
    const chords = await fileService.getChordsFiles();
    console.log()
    setSongChords(chords.song_chords);
    setUserChords(chords.user_chords);

  }
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>, setFileContent: React.Dispatch<React.SetStateAction<string | null>>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setFileContent(event.target?.result as string);
      };
      reader.readAsText(file);
    }
  };

  const highlightDifferences = (text1: string, text2: string) => {
    const differences = diffWords(text1, text2);
    return differences.map((part, index) => {
      if (part.added) {
        return <span key={index} className="added">{part.value}</span>;
      } else if (!part.removed) {
        return <span key={index}>{part.value}</span>;
      } else {
        return null; // Skip parts that are only in text1 (removed parts)
      }
    });
  };

  return (
    <div className="file-comparison" style={{backgroundImage:`url(${bg})`}}>
      <div className="comparison-section">
        <div className="file-content">
          <h3>Song Chords</h3><br/>
          <div className="content">{songChords}</div>
        </div>
        <div className="file-content">
          <h3>Your Chords</h3><br/>
          <div className="content">{userChords && songChords && highlightDifferences(songChords, userChords)}</div>
        </div>
      </div>
    </div>
  );
};

export default FileComparison;
