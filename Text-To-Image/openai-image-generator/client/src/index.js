import React from 'react';
import ReactDOM from 'react-dom';
import App from 'App.js';
import './App.css';

const root = document.getElementById('root');
const reactRoot = ReactDOM.createRoot(root);
reactRoot.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
