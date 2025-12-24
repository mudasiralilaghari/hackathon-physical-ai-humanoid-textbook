// Simple script to add the chatbot to the page
document.addEventListener('DOMContentLoaded', function() {
  // Create the chatbot container
  const chatbotContainer = document.createElement('div');
  chatbotContainer.className = 'chatbotContainer';
  chatbotContainer.innerHTML = `
    <button class="chatbotToggleButton">💬 Chat</button>
    <div class="chatbotWindow" style="display:none;">
      <div class="chatbotHeader">
        <h3>RAG Chatbot</h3>
        <button class="closeButton" style="background: none; border: none; font-size: 24px; cursor: pointer;">×</button>
      </div>
      <div class="chatbotMessages" style="height: 70%; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; gap: 10px;">
        <div class="message botMessage" style="padding: 10px; border-radius: 8px; max-width: 80%; background-color: #f1f1f1; align-self: flex-start;">
          Hello! I'm your RAG chatbot for the Physical AI & Humanoid Robotics textbook. Ask me anything about the content!
        </div>
      </div>
      <div class="chatbotInputContainer" style="display: flex; padding: 10px; border-top: 1px solid #ddd;">
        <textarea id="chatbot-input" placeholder="Ask about the textbook content..." rows="2" style="flex-grow: 1; border: 1px solid #ccc; border-radius: 5px; padding: 8px; margin-right: 10px;"></textarea>
        <button id="chatbot-send" style="background-color: #007bff; color: white; border: none; border-radius: 5px; padding: 8px 12px; cursor: pointer;">Send</button>
      </div>
    </div>
  `;

  // Add to the body
  document.body.appendChild(chatbotContainer);

  // Add basic functionality
  const toggleButton = document.querySelector('.chatbotToggleButton');
  const chatWindow = document.querySelector('.chatbotWindow');
  const closeButton = document.querySelector('.closeButton');
  const input = document.getElementById('chatbot-input');
  const sendButton = document.getElementById('chatbot-send');
  const messagesContainer = document.querySelector('.chatbotMessages');

  // Toggle chat window
  toggleButton.addEventListener('click', function() {
    chatWindow.style.display = 'block';
  });

  // Close chat window
  closeButton.addEventListener('click', function() {
    chatWindow.style.display = 'none';
  });

  // Send message functionality
  function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'message userMessage';
    userMessage.style.cssText = 'padding: 10px; border-radius: 8px; max-width: 80%; background-color: #d1e7ff; align-self: flex-end;';
    userMessage.textContent = message;
    messagesContainer.appendChild(userMessage);

    // Clear input
    input.value = '';

    // Simulate bot response (replace with actual API call)
    setTimeout(() => {
      const botMessage = document.createElement('div');
      botMessage.className = 'message botMessage';
      botMessage.style.cssText = 'padding: 10px; border-radius: 8px; max-width: 80%; background-color: #f1f1f1; align-self: flex-start;';
      botMessage.textContent = 'Processing your question...';
      messagesContainer.appendChild(botMessage);
      
      // Scroll to bottom
      messagesContainer.scrollTop = messagesContainer.scrollHeight;

      // Make actual API call to your backend
      fetch('https://fazalahmed.hf.space/rag/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
          selected_text: null
        })
      })
      .then(response => response.json())
      .then(data => {
        // Remove the "Processing" message
        botMessage.textContent = data.response || "Sorry, I couldn't process your request.";
      })
      .catch(error => {
        botMessage.textContent = "Sorry, there was an error connecting to the RAG service.";
      });
    }, 1000);
  }

  // Send button click event
  sendButton.addEventListener('click', sendMessage);

  // Enter key to send message (with shift for new line)
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
});