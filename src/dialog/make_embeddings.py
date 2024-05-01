import csv
import re

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents import Document

from dialog.settings import vectordb_settings
from dialog.vectorstore import get_vectorstore
from langchain_core.vectorstores import VectorStore


def _get_csv_cols(path: str):
    with open(path) as f:
        reader = csv.DictReader(f)
        return reader.fieldnames


def make_embeddings(
    path: str, embedding_columns=None, metadata_columns=None
):
    embedding_columns = embedding_columns or vectordb_settings.embedding_cols
    metadata_columns = metadata_columns or [
        col for col in _get_csv_cols(path) if col not in embedding_columns
    ]
    print(
        f"Metadata columns: {metadata_columns}\nEmbedding columns: {embedding_columns}"
    )
    loader = CSVLoader(path, metadata_columns=metadata_columns)
    docs = loader.load()
    print(f"Glimpse over the first doc: {docs[0].page_content[:100]}...")

    vectordb: VectorStore = get_vectorstore()
    vectordb.delete_collection()
    vectordb.create_collection()
    vectordb.add_documents(docs)
    print(f"Added {len(docs)} documents to the store.")


if __name__ == "__main__":
    make_embeddings(path=str(vectordb_settings.knowledge_base_path))
