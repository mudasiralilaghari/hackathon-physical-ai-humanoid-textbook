---
id: 005
title: Integrate Chatbot UI with Docusaurus
stage: green
date: 2025-12-24
surface: agent
model: claude-code
feature: chatbot-frontend
branch: 001-docusaurus-rag-integration
user: Mudasir Ali
command: Integrate RAG chatbot UI into Docusaurus textbook
labels: ["frontend", "chatbot", "docusaurus", "react"]
links:
  spec: specs/001-docusaurus-rag-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/components/Chatbot/index.js
  - src/pages/index.js
  - static/chatbot.css
  - static/chatbot.js
  - docusaurus.config.js
tests:
  - npm run start
---

## Prompt

Integrate the RAG chatbot UI into the Docusaurus textbook site so users can ask questions about the content while reading.

## Response snapshot

Implemented chatbot integration with multiple approaches:

### Final Approach: Layout Override with preBodyTags
- Used Docusaurus Layout component override
- Added chatbot via preBodyTags in docusaurus.config.js
- Inline scripts for reliable injection

### Chatbot Features
- Floating toggle button (bottom-right corner)
- Collapsible chat window
- Message history display
- Text input with send button
- Enter key to send (Shift+Enter for new line)

### Backend Integration
- Fetch API calls to RAG backend
- Default URL: https://fazalahmed.hf.space/rag/query
- Handles connection errors gracefully
- Shows processing status to user

### Styling
- Custom CSS for chatbot window
- Responsive design
- Blue theme matching textbook branding
- Smooth animations for open/close

### Alternative Approaches Tried
1. Static JS/CSS files - had import issues
2. Layout override with script injection
3. preBodyTags with inline scripts (final solution)

## Outcome

- ✅ Impact: Chatbot fully integrated into textbook site
- 🧪 Tests: Chatbot appears on all pages, communicates with backend
- 📁 Files: src/components/Chatbot/, static/chatbot.css, static/chatbot.js
- 🔁 Next prompts: Deploy to GitHub Pages, test end-to-end
- 🧠 Reflection: Docusaurus customization requires understanding of React component lifecycle

## Evaluation notes (flywheel)

- Failure modes observed: CSS import issues resolved with inline styles
- Graders run and results: Chatbot renders correctly on all pages
- Prompt variant: Multiple approaches tested before final solution
- Next experiment: Production deployment
