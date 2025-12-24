from abc import ABC, abstractmethod
from src.models.rag_models import QueryRequest, QueryResponse


class Agent(ABC):
    @abstractmethod
    async def answer(self, query_request: QueryRequest) -> QueryResponse:
        """
        The main method for an agent to process a query and return a response.
        """
        pass
