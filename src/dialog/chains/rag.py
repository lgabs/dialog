from operator import itemgetter

from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain.schema.runnable import RunnablePassthrough

from dialog.settings import chain_settings
from dialog.vectorstore import get_retriever, combine_documents


# Prompts
prompts = chain_settings.chain_params.get("prompts")

ANSWER_TEMPLATE = prompts.get("answer_template")
ANSWER_PROMPT = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)

# LLM (for main task)
MODEL_PARAMS = chain_settings.chain_params.get("model_params", {})
llm = ChatOpenAI(
    **MODEL_PARAMS, openai_api_key=chain_settings.openai_api_key.get_secret_value()
)

# Retriever
retriever = get_retriever()


class InputChat(TypedDict):
    """Question for the chat endpoint."""

    question: str
    """Human question."""


rag_chain = (
    (
        {
            "context": itemgetter("question") | retriever | combine_documents,
            "question": RunnablePassthrough(),
        }
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )
    .with_types(input_type=InputChat)
    .with_config({"run_name": "RagChain"})
)
