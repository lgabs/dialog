from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings

from dialog.settings import DATABASE_URL, COLLECTION_NAME

embeddings = OpenAIEmbeddings()

def get_retriever():
    return PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=DATABASE_URL,
        embedding_function=embeddings,
    ).as_retriever()