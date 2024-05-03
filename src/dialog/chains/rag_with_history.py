from operator import itemgetter

from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain.schema.runnable import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableBranch,
    RunnableLambda,
)

from langchain_core.runnables.history import RunnableWithMessageHistory

from dialog.settings import chain_settings
from dialog.memory import get_message_history, format_chat_history
from dialog.vectorstore import get_retriever, combine_documents


# Prompts
prompts = chain_settings.chain_params.get("prompts")
STANDALONE_QUESTION_TEMPLATE = prompts.get("standalone_question_template")
STANDALONE_QUESTION_PROMPT = PromptTemplate.from_template(STANDALONE_QUESTION_TEMPLATE)

ANSWER_TEMPLATE = prompts.get("answer_template")
ANSWER_PROMPT = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)

# Standalone Question

_standalone_question = RunnableBranch(
    # If input includes chat_history, we condense it with the follow-up question
    (
        RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
            run_name="HasChatHistoryCheck"
        ),  # Condense follow-up question and chat into a standalone_question
        RunnablePassthrough.assign(
            chat_history=lambda x: format_chat_history(x["chat_history"])
        ).with_config(run_name="ChatHistory")
        | STANDALONE_QUESTION_PROMPT
        | ChatOpenAI(temperature=0)
        | StrOutputParser(),
    ),
    # Else, we have no chat history, so just pass through the question
    RunnableLambda(itemgetter("question")).with_config(
        run_name="QuestionWithoutHistory"
    ),
) | ({"question": RunnablePassthrough()})

# LLM (for main task)
MODEL_PARAMS = chain_settings.chain_params.get("model_params", {})
llm = ChatOpenAI(
    **MODEL_PARAMS, openai_api_key=chain_settings.openai_api_key.get_secret_value()
)

# Retriever
retriever = get_retriever()

# Build the chain
_query_with_context = RunnableParallel(
    {
        "context": itemgetter("question") | retriever | combine_documents,
        "question": lambda x: x["question"],
    }
)


conversational_qa_chain = (
    _standalone_question.with_config({"run_name": "StandaloneQuestion"})
    | _query_with_context.with_config({"run_name": "QuestionWithContext"})
    | ANSWER_PROMPT.with_config({"run_name": "FinalAnswerPrompt"})
    | llm
    | StrOutputParser()
)


class InputChat(TypedDict):
    """Question for the chat endpoint."""

    question: str
    """Human question."""


rag_with_history_chain = (
    RunnableWithMessageHistory(
        conversational_qa_chain,
        get_message_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
    .with_types(input_type=InputChat)
    .with_config({"run_name": "RagChainWithHistory"})
)
