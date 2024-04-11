import React from 'react';
import './App.css';
import Chatbot from 'react-chatbot-kit'
import 'react-chatbot-kit/build/main.css'

import config from '../src/config.js';
import MessageParser from '../src/MessageParser.jsx';
import ActionProvider from '../src/ActionProvider.jsx';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Verse</h1>
        <Chatbot
          config={config}
          messageParser={MessageParser}
          actionProvider={ActionProvider} />
      </header>
    </div>
  );
}

export default App;
