import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chatbot from '@site/src/components/Chatbot';

const ChatbotLayout = (props) => {
  const { children } = props;

  return (
    <>
      <OriginalLayout {...props}>{children}</OriginalLayout>
      <Chatbot />
    </>
  );
};

export default ChatbotLayout;