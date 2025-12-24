// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'An AI-native textbook',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://mudasiralilaghari.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<username>.github.io/<repoName>/'
  baseUrl: '/hackathon-physical-ai-humanoid-textbook/',

  // GitHub pages deployment config.
  organizationName: 'mudasiralilaghari', // Usually your GitHub org/user name.
  projectName: 'hackathon-physical-ai-humanoid-textbook', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/mudasiralilaghari/hackathon-physical-ai-humanoid-textbook/tree/main/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],


  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Add the chatbot directly to the HTML head and body
      headTags: [
        {
          tagName: 'style',
          attributes: {
            type: 'text/css',
          },
          innerHTML: `
            .chatbotContainer {
              position: fixed;
              bottom: 20px;
              right: 20px;
              z-index: 1000;
            }
            .chatbotToggleButton {
              background-color: #007bff;
              color: white;
              border: none;
              border-radius: 50%;
              width: 60px;
              height: 60px;
              font-size: 16px;
              cursor: pointer;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .chatbotWindow {
              width: 350px;
              height: 500px;
              background-color: white;
              border-radius: 10px;
              box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
              display: flex;
              flex-direction: column;
              overflow: hidden;
              position: absolute;
              bottom: 70px;
              right: 0;
            }
            .chatbotHeader {
              background-color: #007bff;
              color: white;
              padding: 10px;
              text-align: center;
              display: flex;
              justify-content: space-between;
              align-items: center;
            }
            .chatbotMessages {
              flex-grow: 1;
              padding: 10px;
              overflow-y: auto;
              display: flex;
              flex-direction: column;
              gap: 10px;
            }
            .message {
              padding: 10px;
              border-radius: 8px;
              max-width: 80%;
            }
            .botMessage {
              background-color: #f1f1f1;
              align-self: flex-start;
            }
            .userMessage {
              background-color: #d1e7ff;
              align-self: flex-end;
            }
            .chatbotInputContainer {
              display: flex;
              padding: 10px;
              border-top: 1px solid #ddd;
            }
            .chatbotInputContainer input {
              flex-grow: 1;
              border: 1px solid #ccc;
              border-radius: 5px;
              padding: 8px;
            }
            .chatbotInputContainer button {
              background-color: #007bff;
              color: white;
              border: none;
              border-radius: 5px;
              padding: 8px 12px;
              margin-left: 10px;
              cursor: pointer;
            }
            .closeButton {
              background: none;
              border: none;
              font-size: 24px;
              cursor: pointer;
              color: white;
              padding: 0;
              width: 30px;
              height: 30px;
              display: flex;
              align-items: center;
              justify-content: center;
            }
          `,
        },
      ],
      // Add the chatbot HTML directly to the body
      preBodyTags: [
        {
          tagName: 'div',
          attributes: {
            id: 'chatbot-root'
          },
          innerHTML: `
            <div class="chatbotContainer" style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
              <button class="chatbotToggleButton" style="background-color: #007bff; color: white; border: none; border-radius: 50%; width: 60px; height: 60px; font-size: 16px; cursor: pointer; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
                💬 Chat
              </button>
              <div class="chatbotWindow" style="display:none; width: 350px; height: 500px; background-color: white; border-radius: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); display: flex; flex-direction: column; overflow: hidden; position: absolute; bottom: 70px; right: 0;">
                <div class="chatbotHeader" style="background-color: #007bff; color: white; padding: 10px; text-align: center; display: flex; justify-content: space-between; align-items: center;">
                  <h3 style="margin: 0;">RAG Chatbot</h3>
                  <button class="closeButton" style="background: none; border: none; font-size: 24px; cursor: pointer; color: white; padding: 0; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">×</button>
                </div>
                <div class="chatbotMessages" style="flex-grow: 1; padding: 10px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;">
                  <div class="message botMessage" style="padding: 10px; border-radius: 8px; max-width: 80%; background-color: #f1f1f1; align-self: flex-start;">
                    Hello! I'm your RAG chatbot for the Physical AI & Humanoid Robotics textbook. Ask me anything about the content!
                  </div>
                </div>
                <div class="chatbotInputContainer" style="display: flex; padding: 10px; border-top: 1px solid #ddd;">
                  <textarea id="chatbot-input" placeholder="Ask about the textbook content..." rows="2" style="flex-grow: 1; border: 1px solid #ccc; border-radius: 5px; padding: 8px; margin-right: 10px;"></textarea>
                  <button id="chatbot-send" style="background-color: #007bff; color: white; border: none; border-radius: 5px; padding: 8px 12px; cursor: pointer;">Send</button>
                </div>
              </div>
            </div>
          `,
        },
      ],
      scripts: [
        {
          tagName: 'script',
          innerHTML: `
            document.addEventListener('DOMContentLoaded', function() {
              // Add functionality to the chatbot
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

                // Show processing message
                const processingMessage = document.createElement('div');
                processingMessage.className = 'message botMessage';
                processingMessage.style.cssText = 'padding: 10px; border-radius: 8px; max-width: 80%; background-color: #f1f1f1; align-self: flex-start;';
                processingMessage.textContent = 'Processing your question...';
                messagesContainer.appendChild(processingMessage);

                // Scroll to bottom
                messagesContainer.scrollTop = messagesContainer.scrollHeight;

                // Make API call to your backend
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
                  // Update the processing message with the actual response
                  processingMessage.textContent = data.response || "Sorry, I couldn't process your request.";
                })
                .catch(error => {
                  processingMessage.textContent = "Sorry, there was an error connecting to the RAG service.";
                });
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
          `,
        }
      ],
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: '🤖 Physical AI & Humanoid Robotics Textbook',
        logo: {

          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'textbookSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/mudasiralilaghari/hackathon-physical-ai-humanoid-textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Content',
            items: [
              {
                label: 'Textbook Home',
                to: '/',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/mudasiralilaghari/hackathon-physical-ai-humanoid-textbook',
              },
            ],
          },
        ],
        copyright: `Physical AI & Humanoid Robotics Textbook build by Mudasir Ali. Copyright © 2025.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
