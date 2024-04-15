from operator import itemgetter
from typing import List, Tuple

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.schema import format_document

from langserve.pydantic_v1 import BaseModel, Field

from dialog.settings import PROJECT_CONFIG, OPENAI_API_KEY
from dialog.llm.memory import generate_memory_instance


# Prompts

condense_question_template = PROJECT_CONFIG.get("prompt").get(
    "condense_question_template"
)
condense_question_prompt = PromptTemplate.from_template(condense_question_template)

final_answer_template = PROJECT_CONFIG.get("prompt").get("final_answer_template")
final_answer_prompt = ChatPromptTemplate.from_template(final_answer_template)

default_document_prompt = PromptTemplate.from_template(template="{page_content}")

# History
def _format_chat_history(chat_history: List[Tuple]) -> str:
    """Format chat history into a string."""
    buffer = ""
    for dialogue_turn in chat_history:
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]
        buffer += "\n" + "\n".join([human, ai])
    return buffer


# Retriever


def _combine_documents(
    docs, document_prompt=default_document_prompt, document_separator="\n\n"
):
    """Combine documents into a single string."""
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

# LLM

llm = ChatOpenAI(**PROJECT_CONFIG.get("model", {}), openai_api_key=OPENAI_API_KEY)


# Build the Chain
_inputs = RunnableMap(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: _format_chat_history(x["chat_history"])
    )
    | condense_question_prompt
    | llm
    | StrOutputParser(),
)

_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": lambda x: x["standalone_question"],
}

conversational_qa_chain = (
    _inputs | _context | final_answer_prompt | llm | StrOutputParser()
)


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    # As of 2024-02-05, this chat widget is not fully supported.
    question: str = Field(
        ...,
        description="The human input to the chat system.",
        extra={"widget": {"type": "chat", "input": "question"}},
    )


chain_with_history = RunnableWithMessageHistory(
    conversational_qa_chain,
    generate_memory_instance,
    input_messages_key="question",
    history_messages_key="history",
).with_types(input_type=InputChat)
