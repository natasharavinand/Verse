// Adapted from react-chatbox-kit documentation (https://fredrikoseberg.github.io/react-chatbot-kit-docs/docs/)

import React from 'react';
import { createChatBotMessage } from 'react-chatbot-kit';
import BotAvatar from './components/BotAvatar/BotAvatar';
import CourseOptions from './components/CourseOptions/CourseOptions'
import Recommendation from './components/Recommendation/Recommendation';

const config = {
  botName: 'your Yale English Literature Professor',
  customComponents: {
    botAvatar: (props) => <BotAvatar {...props} />
  },
  initialMessages: [createChatBotMessage('Hello! Welcome to your Yale English Literature course. What would you like to discuss today?', {
    widget: 'course options'
  })],
  customStyles: {
    botMessageBox: {
      backgroundColor: '#2e69b2',
    },
    chatButton: {
      backgroundColor: '#2e69b2',
    },
  },
  widgets: [
    {
      widgetName: 'course options',
      widgetFunc: (props) => <CourseOptions {...props} />,
    },
    {
      widgetName: 'recommendation',
      widgetFunc: (props) => <Recommendation {...props} />,
    },
  ],
};

export default config;