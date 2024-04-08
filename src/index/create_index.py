from src.index.create_data_store import create_data_store
from src.index.create_app import create_doc_search_app
from src.index.ingest_data import ingest_documents
from src.config.logging import logger


def create_index_for_document_search() -> None:
    """
    This function orchestrates the creation of an index for document search.
    It follows a three-step process:
    1. Creating a data store.
    2. Ingesting documents into the data store.
    3. Creating a search application using the ingested documents.
    """
    logger.info("Starting the index creation process for document search.")

    # step 1: Create data store
    logger.info("Creating data store.")
    create_data_store()

    # step 2: Ingest documents
    logger.info("Ingesting documents.")
    ingest_documents()

    # step 3: Create document search app
    logger.info("Creating document search application.")
    create_doc_search_app()

    logger.info("Index creation process completed successfully.")


if __name__ == '__main__':
    create_index_for_document_search()
