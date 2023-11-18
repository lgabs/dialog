from typing import List

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from llm.memory import CustomPostgresChatMessageHistory
from models import CompanyContent
from models.db import session
from settings import DATABASE_URL, OPENAI_API_KEY, PROJECT_CONFIG, VERBOSE_LLM
from sqlalchemy import asc, select

CHAT_LLM = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-3.5-turbo",
    temperature=0.2,
)
EMBEDDINGS_LLM = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
PROMPT = PROJECT_CONFIG.get("prompt")


def generate_embeddings(documents: List[str]):
    """
    Generate embeddings for a list of documents
    """
    return EMBEDDINGS_LLM.embed_documents(documents)


def generate_embedding(document: str):
    """
    Generate embeddings for a single instance of document
    """
    return EMBEDDINGS_LLM.embed_query(document)


def get_most_relevant_contents_from_message(message, top=5):
    message_embedding = generate_embedding(message)
    possible_contents = session.scalars(
        select(CompanyContent).filter(
            CompanyContent.embedding.l2_distance(message_embedding) < 5
        ).order_by(
            asc(
                CompanyContent.embedding.l2_distance(message_embedding)
            )
        ).limit(top)
    ).all()
    possible_contents = possible_contents
    return possible_contents


def generate_memory_instance(session_id):
    """
    Generate a memory instance for a given session_id
    """
    return CustomPostgresChatMessageHistory(
        connection_string=DATABASE_URL,
        session_id=session_id,
        table_name="chat_messages"
    )


def add_user_message_to_message_history(
        session_id, message, memory=None
):
    """
    Add a user message to the message history and returns the updated
    memory instance
    """
    if not memory:
        memory = generate_memory_instance(session_id)

    memory.add_user_message(message)
    return memory


def get_messages(session_id):
    """
    Get all messages for a given session_id
    """
    memory = generate_memory_instance(session_id)
    return memory.messages


def process_user_intent(
        session_id, message
):
    """
    Process user intent using memory and embeddings
    """
    # top 2 most relevant contents
    relevant_contents = get_most_relevant_contents_from_message(message, top=2)

    suggested_content = "\n\n".join([f"{c.question}\n{c.content}\n\n"
                                     for c in relevant_contents])

    prompt_templating = [
        SystemMessagePromptTemplate.from_template(PROMPT.get("header")),
        MessagesPlaceholder(variable_name="chat_history"),
    ]

    if len(relevant_contents) > 0:
        prompt_templating.append(
            SystemMessagePromptTemplate.from_template(
                f"{PROMPT.get('suggested')}\n\n{suggested_content}"
            )
        )

    prompt_templating.append(
        HumanMessagePromptTemplate.from_template("{user_message}"))

    prompt = ChatPromptTemplate(
        messages=prompt_templating
    )

    psql_memory = generate_memory_instance(session_id)
    conversation = LLMChain(
        llm=CHAT_LLM,
        prompt=prompt,
        verbose=VERBOSE_LLM
    )
    ai_message = conversation({
        "user_message": message,
        "chat_history": psql_memory.messages
    })
    psql_memory.add_user_message(message)
    psql_memory.add_ai_message(ai_message["text"])

    return ai_message
