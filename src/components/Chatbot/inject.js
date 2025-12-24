import React from 'react';
import { createRoot } from 'react-dom/client';
import Chatbot from './index';

// Function to inject the chatbot component
function injectChatbot() {
  // Create a container for the chatbot
  const chatbotContainer = document.createElement('div');
  chatbotContainer.id = 'chatbot-root';
  document.body.appendChild(chatbotContainer);

  // Render the chatbot component
  const root = createRoot(chatbotContainer);
  root.render(<Chatbot />);
}

// Check if the DOM is already loaded or wait for it
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectChatbot);
} else {
  // DOM is already loaded, run immediately
  injectChatbot();
}

export default injectChatbot;