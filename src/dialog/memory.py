from typing import List, Union
from dialog.settings import memory_settings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_message_histories import PostgresChatMessageHistory
import uuid


def format_chat_history(
    chat_history: List[Union[HumanMessage, AIMessage, SystemMessage]]
) -> str:
    """Format chat history into a string."""
    buffer = ""
    for message in chat_history:
        buffer += "\n" + f"{message.type}: {message.content}"
    return buffer


def get_message_history(session_id: str = None) -> PostgresChatMessageHistory:
    session_id = session_id or str(uuid.uuid4())
    return PostgresChatMessageHistory(
        session_id=session_id, connection_string=str(memory_settings.memory_connection)
    )
