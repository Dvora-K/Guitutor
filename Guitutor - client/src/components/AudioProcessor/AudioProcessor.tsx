import React, { useState, useEffect } from 'react';
import * as d3 from 'd3';

const AudioProcessor: React.FC = () => {
  const [audioData, setAudioData] = useState<Float32Array | null>(null);
  const [audioContext, setAudioContext] = useState<AudioContext | null>(null);

  useEffect(() => {
    if (!audioContext) {
      setAudioContext(new AudioContext());
    } else {
      fetchAudioFile();
    }
  }, [audioContext]);

  const fetchAudioFile = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_vocal');
      console.log(response)
      const arrayBuffer = await response.arrayBuffer();

      if (audioContext) {
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        const channelData = audioBuffer.getChannelData(0); // Assuming mono audio
        setAudioData(channelData);
      }
    } catch (error) {
      console.error('Error fetching the audio file:', error);
    }
  };

  const drawWaveform = () => {
    if (!audioData) return;

    const svg = d3.select('#waveform')
      .attr('width', 800)
      .attr('height', 200);

    const width = 800;
    const height = 200;
    const x = d3.scaleLinear().domain([0, audioData.length]).range([0, width]);
    const y = d3.scaleLinear().domain([-1, 1]).range([height, 0]);

    const line = d3.line<number>()
      .x((d, i) => x(i))
      .y(d => y(d));

    svg.selectAll('*').remove(); // Clear previous waveform

    svg.append('path')
      .datum(audioData)
      .attr('d', line)
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 1)
      .attr('fill', 'none');
  };

  useEffect(() => {
    drawWaveform();
  }, [audioData]);

  return (
    <div>
      <svg id="waveform"></svg>
    </div>
  );
};

export default AudioProcessor;
