from operator import itemgetter

from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain.schema.runnable import RunnableMap, RunnablePassthrough

from langchain_core.runnables.history import RunnableWithMessageHistory

from dialog.settings import chain_settings
from dialog.memory import get_message_history, format_chat_history
from dialog.retriever import get_retriever, combine_documents


# Prompts
prompts = chain_settings.chain_params.get("prompts")
STANDALONE_QUESTION_TEMPLATE = prompts.get("standalone_question_template")
STANDALONE_QUESTION_PROMPT = PromptTemplate.from_template(STANDALONE_QUESTION_TEMPLATE)

FINAL_ANSWER_TEMPLATE = prompts.get("final_answer_template")
FINAL_ANSWER_PROMPT = ChatPromptTemplate.from_template(FINAL_ANSWER_TEMPLATE)

_inputs = RunnableMap(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: format_chat_history(x["chat_history"])
    )
    | STANDALONE_QUESTION_PROMPT
    | ChatOpenAI(temperature=0)
    | StrOutputParser(),
)

# LLM (for main task)
MODEL_PARAMS = chain_settings.chain_params.get("model_params", {})
llm = ChatOpenAI(
    **MODEL_PARAMS, openai_api_key=chain_settings.openai_api_key.get_secret_value()
)

# Retriever
retriever = get_retriever()

# Build the chain
_context = {
    "context": itemgetter("standalone_question") | retriever | combine_documents,
    "question": lambda x: x["standalone_question"],
}


conversational_qa_chain = (
    _inputs | _context | FINAL_ANSWER_PROMPT | llm | StrOutputParser()
)


class InputChat(TypedDict):
    """Input for the chat endpoint."""

    human_input: str
    """Human input"""


rag_with_history_chain = RunnableWithMessageHistory(
    conversational_qa_chain,
    get_message_history,
    input_messages_key="human_input",
    history_messages_key="history",
).with_types(input_type=InputChat)
