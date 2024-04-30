import csv
import logging

from langchain_community.document_loaders.csv_loader import CSVLoader

from dialog.settings import settings, vectordb_settings
from dialog.vectorstore import get_vectorstore
logging.basicConfig(level=settings.logging_level.upper())

EMBEDDING_COLUMNS = ["Document"]


def _get_csv_cols(path: str):
    with open(path) as f:
        reader = csv.DictReader(f)
        return reader.fieldnames


def make_embeddings(
    path: str, embedding_columns=EMBEDDING_COLUMNS, metadata_columns=None
):
    metadata_columns = metadata_columns or [
        col for col in _get_csv_cols(path) if col not in embedding_columns
    ]
    logging.debug(
        f"Metadata columns: {metadata_columns}\nEmbedding columns: {embedding_columns}"
    )
    loader = CSVLoader(path, metadata_columns=metadata_columns)
    docs = loader.load()

    vectordb = get_vectorstore()
    vectordb.add_documents(docs)
    logging.debug(f"Added {len(docs)} documents to the store.")


if __name__ == "__main__":
    make_embeddings(path=str(vectordb_settings.knowledge_base_path))
