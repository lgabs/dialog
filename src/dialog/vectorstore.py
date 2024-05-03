from langchain.schema import format_document
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from dialog.settings import vectordb_settings

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    """Combine documents into a single string."""
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def get_vectorstore():
    return PGVector(
        collection_name=vectordb_settings.collection_name,
        connection=str(vectordb_settings.vectordb_connection),
        embeddings=OpenAIEmbeddings(),
        create_extension=False,
    )


def get_retriever():
    return get_vectorstore().as_retriever()
