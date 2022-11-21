import React from 'react';
import '../styles/SingleNews.css';
import Hero from '../components/SingleNews/Hero';
import Maine from '../components/SingleNews/Maine';

export default function SingleNews() {
  return (
    <div className="home">
      <Hero />
      <Maine />
    </div>
  );
}
