import React, { useState, useEffect } from 'react';
import './styles.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your RAG chatbot for the Physical AI & Humanoid Robotics textbook. Ask me anything about the content!", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('https://fazalahmed.hf.space/rag/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: inputValue,
          selected_text: null
        })
      });

      const data = await response.json();
      
      const botMessage = { 
        id: Date.now() + 1, 
        text: data.response || "Sorry, I couldn't process your request.", 
        sender: 'bot' 
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { 
        id: Date.now() + 1, 
        text: "Sorry, there was an error connecting to the RAG service.", 
        sender: 'bot' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chatbotContainer">
      {isOpen ? (
        <div className="chatbotWindow">
          <div className="chatbotHeader">
            <h3>RAG Chatbot</h3>
            <button onClick={toggleChat} className="closeButton">×</button>
          </div>
          <div className="chatbotMessages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender === 'bot' ? 'botMessage' : 'userMessage'}`}
              >
                {message.text}
              </div>
            ))}
            {isLoading && (
              <div className="message botMessage">
                Thinking...
              </div>
            )}
          </div>
          <div className="chatbotInputContainer">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the textbook content..."
              rows="2"
            />
            <button onClick={sendMessage} disabled={isLoading}>Send</button>
          </div>
        </div>
      ) : (
        <button className="chatbotToggleButton" onClick={toggleChat}>
          💬 Chat
        </button>
      )}
    </div>
  );
};

export default Chatbot;