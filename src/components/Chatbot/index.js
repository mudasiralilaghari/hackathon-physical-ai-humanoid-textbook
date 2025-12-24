import React, { useState, useEffect } from 'react';

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
    <div
      className="chatbotContainer"
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 1000
      }}
    >
      {isOpen ? (
        <div
          className="chatbotWindow"
          style={{
            width: '350px',
            height: '500px',
            backgroundColor: 'white',
            borderRadius: '10px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden'
          }}
        >
          <div
            className="chatbotHeader"
            style={{
              backgroundColor: '#007bff',
              color: 'white',
              padding: '10px',
              textAlign: 'center'
            }}
          >
            <h3>RAG Chatbot</h3>
            <button
              onClick={toggleChat}
              className="closeButton"
              style={{
                background: 'none',
                border: 'none',
                fontSize: '24px',
                cursor: 'pointer',
                color: 'white',
                padding: 0,
                width: '30px',
                height: '30px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              ×
            </button>
          </div>
          <div
            className="chatbotMessages"
            style={{
              flexGrow: 1,
              padding: '10px',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px'
            }}
          >
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender === 'bot' ? 'botMessage' : 'userMessage'}`}
                style={{
                  padding: '10px',
                  borderRadius: '8px',
                  maxWidth: '80%',
                  backgroundColor: message.sender === 'bot' ? '#f1f1f1' : '#d1e7ff',
                  alignSelf: message.sender === 'bot' ? 'flex-start' : 'flex-end'
                }}
              >
                {message.text}
              </div>
            ))}
            {isLoading && (
              <div
                className="message botMessage"
                style={{
                  padding: '10px',
                  borderRadius: '8px',
                  maxWidth: '80%',
                  backgroundColor: '#f1f1f1',
                  alignSelf: 'flex-start'
                }}
              >
                Thinking...
              </div>
            )}
          </div>
          <div
            className="chatbotInputContainer"
            style={{
              display: 'flex',
              padding: '10px',
              borderTop: '1px solid #ddd'
            }}
          >
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the textbook content..."
              rows="2"
              style={{
                flexGrow: 1,
                border: '1px solid #ccc',
                borderRadius: '5px',
                padding: '8px',
                marginRight: '10px'
              }}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading}
              style={{
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                padding: '8px 12px',
                cursor: isLoading ? 'not-allowed' : 'pointer'
              }}
            >
              Send
            </button>
          </div>
        </div>
      ) : (
        <button
          className="chatbotToggleButton"
          style={{
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            width: '60px',
            height: '60px',
            fontSize: '16px',
            cursor: 'pointer',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'
          }}
          onClick={toggleChat}
        >
          💬 Chat
        </button>
      )}
    </div>
  );
};

export default Chatbot;