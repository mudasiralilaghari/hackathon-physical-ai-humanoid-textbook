from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ChatHistory(session_id='{self.session_id}', user_message='{self.user_message[:20]}...', assistant_message='{self.assistant_message[:20]}...')>"
