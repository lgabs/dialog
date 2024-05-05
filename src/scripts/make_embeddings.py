#! /usr/bin/env python
import csv
import re

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents import Document

from dialog.settings import vectordb_settings, settings
from dialog.vectorstore import get_vectorstore
from langchain_core.vectorstores import VectorStore

import logging

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("make_embeddings")


def _get_csv_cols(path: str):
    with open(path) as f:
        reader = csv.DictReader(f)
        return reader.fieldnames


def make_embeddings(path: str):
    embedding_columns = vectordb_settings.embedding_cols
    metadata_columns = [
        col for col in _get_csv_cols(path) if col not in embedding_columns
    ]

    logger.info("Metadata columns: %s", metadata_columns)
    logger.info("Embedding columns: %s", embedding_columns)

    loader = CSVLoader(path, metadata_columns=metadata_columns)
    docs = loader.load()

    logger.debug("Glimpse over the first doc: %s", docs[0].page_content[:100])

    vectordb = get_vectorstore()
    vectordb.delete_collection()
    vectordb.create_collection()
    vectordb.add_documents(docs)

    logger.info(f"Added %s documents to the store.", len(docs))


if __name__ == "__main__":
    logger.debug("knowledge_base_path: %s", vectordb_settings.knowledge_base_path)
    try:
        make_embeddings(path=str(vectordb_settings.knowledge_base_path))
    except Exception as e:
        logger.error(e)
        exit(-1)
    else:
        exit(0)
