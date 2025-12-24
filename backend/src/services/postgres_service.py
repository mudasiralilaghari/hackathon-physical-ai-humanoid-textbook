import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.db_models import Base, ChatHistory
from src.utils.logger import get_logger
from typing import List

logger = get_logger(__name__)

class PostgresService:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            logger.warning("DATABASE_URL environment variable is not set. Chat history functionality will be disabled.")
            self.engine = None
            self.SessionLocal = None
        else:
            self.engine = create_async_engine(self.database_url, echo=False)
            self.SessionLocal = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

    async def create_tables(self):
        if not self.engine:
            logger.info("DATABASE_URL not set, skipping table creation.")
            return

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created.")

    async def get_session(self) -> AsyncSession:
        if not self.SessionLocal:
            raise RuntimeError("DATABASE_URL not set, cannot create session.")
        return self.SessionLocal()

    async def add_chat_history(self, session_id: str, user_message: str, assistant_message: str):
        if not self.engine:
            logger.info(f"DATABASE_URL not set, skipping chat history save for session {session_id}")
            return

        async with self.get_session() as session:
            async with session.begin():
                chat_entry = ChatHistory(
                    session_id=session_id,
                    user_message=user_message,
                    assistant_message=assistant_message
                )
                session.add(chat_entry)
            logger.info(f"Added chat history for session {session_id}")

    async def get_chat_history(self, session_id: str) -> List[ChatHistory]:
        if not self.engine:
            logger.info(f"DATABASE_URL not set, returning empty chat history for session {session_id}")
            return []

        async with self.get_session() as session:
            result = await session.execute(
                ChatHistory.__table__.select().where(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp)
            )
            return result.fetchall()

# Global instance
postgres_service = None

def get_postgres_service():
    global postgres_service
    if postgres_service is None:
        try:
            postgres_service = PostgresService()
        except Exception as e:
            logger.warning(f"Failed to initialize Postgres service: {str(e)}. Chat history will be disabled.")
            # Create a dummy service that handles the no-database case
            postgres_service = PostgresService()  # This will initialize with None values
    return postgres_service
