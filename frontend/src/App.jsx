import React from 'react';
import {
  createBrowserRouter, RouterProvider, Route, createRoutesFromElements,
} from 'react-router-dom';
import Home from './pages/Home';
import ContactUs from './pages/ContactUs';
import AboutUs from './pages/AboutUs';
import Faqs from './pages/Faqs';
import WeatherNews from './pages/WeatherNews';
import Career from './pages/Career';
import Business from './pages/Business';
import Features from './pages/Features';
import Dashboard from './pages/Dashboard';
import AppLayout from './components/AppLayout';
import Notification from './pages/Notification';
import AirQuality from './pages/AirQuality';
import Culture from './pages/Culture';
import SingleNews from './pages/SingleNews';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<AppLayout />}>
      <Route path="/" element={<Home />} />
      <Route path="/business" element={<Business />} />
      <Route path="/careers" element={<Career />} />
      <Route path="/weather-news" element={<WeatherNews />} />
      <Route path="/faqs" element={<Faqs />} />
      <Route path="/about-us" element={<AboutUs />} />
      <Route path="/contact-us" element={<ContactUs />} />
      <Route path="/features" element={<Features />} />
      <Route path="/notification" element={<Notification />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/air-quality" element={<AirQuality />} />
      <Route path="/culture" element={<Culture />} />
      <Route path="/single-news" element={<SingleNews />} />
    </Route>,
  ),
);
export default function App() {
  return (
    <RouterProvider router={router} />
  );
}
