import argparse

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores.pgvector import PGVector

from dialog.settings import COLLECTION_NAME, DATABASE_URL, PROJECT_CONFIG

DEFAULT_METADATA_COLUMNS = PROJECT_CONFIG.get("documents").get("metadata_cols")


def load_csv_and_generate_embeddings(path: str, cleardb: bool, embed_columns: list[str]):
    # TODO: add metadata to the documents and rename content to document
    loader = CSVLoader(path, csv_args={"fieldnames": ["content"]})
    docs = loader.load()

    store = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=DATABASE_URL,
        embedding_function=OpenAIEmbeddings(),
        pre_delete_collection=cleardb
    )
    # TODO: add only new documents using a hash of the document for comparison
    store.add_documents(docs)
    print(f"Added {len(docs)} documents to the store.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=False, default="./know.csv")
    parser.add_argument("--cleardb", action="store_true", default=True)
    parser.add_argument("--embed-columns", default="content")
    args = parser.parse_args()

    load_csv_and_generate_embeddings(
        args.path, args.cleardb, args.embed_columns.split(','))