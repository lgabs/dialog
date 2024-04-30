from typing import List, Tuple
from dialog.settings import settings
from langchain.memory import PostgresChatMessageHistory


def format_chat_history(chat_history: List[Tuple]) -> str:
    """Format chat history into a string."""
    buffer = ""
    for dialogue_turn in chat_history:
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]
        buffer += "\n" + "\n".join([human, ai])
    return buffer


def get_message_history(session_id: str):
    return PostgresChatMessageHistory(
        session_id=session_id, connection_string=str(settings.database_url)
    )
