from src.index.create_data_store import create_data_store
from src.index.create_app import create_doc_search_app
from src.index.ingest_data import ingest_documents
from src.config.logging import logger
from src.config.setup import config


def validate_configuration(config):
    """ Validate the essential configuration parameters. """
    assert config.BUCKET, "Bucket name must be set in the configuration."


def create_index_for_document_search(data_store_display_name, data_store_id, gcs_input_uri):
    """
    Orchestrate the creation of an index for document search.

    The process involves:
    1. Creating a data store with a given display name and identifier.
    2. Ingesting documents from a specified Google Cloud Storage URI into the data store.
    3. Creating a document search application with the newly ingested data.

    Parameters:
        data_store_display_name (str): The display name for the data store.
        data_store_id (str): The unique identifier for the data store.
        gcs_input_uri (str): The Google Cloud Storage URI where the input documents are stored.

    Raises:
        AssertionError: If any of the input parameters are empty.
        Exception: For any errors that occur during the data store creation, document ingestion, or app creation.
    """
    logger.info("Starting the index creation process for document search.")

    try:
        logger.info("Creating data store.")
        create_data_store(data_store_display_name, data_store_id)

        logger.info("Ingesting documents.")
        ingest_documents(gcs_input_uri, data_store_id)

        logger.info("Creating document search application.")
        create_doc_search_app(data_store_display_name, data_store_id)

        logger.info("Index creation process completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during the index creation process: {e}")
        raise


if __name__ == '__main__':
    validate_configuration(config)
    data_store_display_name = 'quarterly-reports-2'
    data_store_id = 'quarterly-reports-2'
    gcs_input_uri = f'gs://{config.BUCKET}/raw_docs/metadata.json'
    create_index_for_document_search(data_store_display_name, data_store_id, gcs_input_uri)
