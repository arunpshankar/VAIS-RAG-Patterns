from google.cloud import discoveryengine_v1beta as discoveryengine
from google.api_core.client_options import ClientOptions
from src.search.utils import extract_relevant_data
from src.search.utils import create_summary_dict
from src.config.logging import logger 
from src.config.setup import config
from typing import Optional
from typing import Dict
from typing import Any


LOCATION = "global" 


def search_data_store(search_query: str, filter_str: str, data_store_id: str) -> Optional[discoveryengine.SearchResponse]:
    """
    Search the data store using Google Cloud's Discovery Engine API.

    Args:
        search_query (str): The search query string.
        filter_str (str): Filter string for the query.
        data_store_id (str): Vertex AI Search Data Store ID.

    Returns:
        Optional[discoveryengine.SearchResponse]: The search response from the Discovery Engine API.
    """
    try:
        client_options = (
            ClientOptions(api_endpoint=f"{LOCATION}-discoveryengine.googleapis.com")
            if LOCATION != "global"
            else None
        )

        client = discoveryengine.SearchServiceClient(client_options=client_options)

        serving_config = client.serving_config_path(
            project=config.PROJECT_ID,
            location=LOCATION,
            data_store=data_store_id,
            serving_config="default_config",
        )

        content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
            snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                return_snippet=False  # snippets are NOT important in the context of this use case
            ),
            extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                max_extractive_answer_count=3,
                max_extractive_segment_count=3,
            ),
            summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
                summary_result_count=5,
                include_citations=True,
                ignore_adversarial_query=False,
                ignore_non_summary_seeking_query=False,
            ),
        )

        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=search_query,
            filter=filter_str,
            page_size=5,
            content_search_spec=content_search_spec,
            query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
                condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
            ),
            spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
                mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
            ),
        )

        response = client.search(request)
        return response

    except Exception as e:
        logger.error(f"Error during data store search: {e}")
        return None


def search(query: str, company: str, time_period: str, data_store_id: str) -> Dict[str, Any]:
    """
    Searches a data store based on a given search query and filter, 
    then consolidates the results in a dictionary.

    Parameters:
    query (str): The query used for searching the data store.
    company (str): The company name.
    time_period (str): The time period.
    data_store_id (str): Vertex AI Search Data Store ID.

    Returns:
    Dict[str, Any]: A dictionary containing the consolidated results of the search.
                    Returns an empty dictionary if an error occurs.
    """
    if company and time_period:
        filter_str = f"company: ANY(\"{company}\") AND time_period: ANY(\"{time_period}\")"
    elif company and not time_period:
        filter_str = f"company: ANY(\"{company}\")"
    elif not company and time_period:
        filter_str = f"time_period: ANY(\"{time_period}\")"
    else:
        filter_str = ""

    try:
        # Perform the search with the provided query and filter
        hits = search_data_store(query, filter_str, data_store_id)

        # Extract relevant data from the search results
        matches = extract_relevant_data(hits)

        # Create a summary dictionary from the matches
        summary_dict = create_summary_dict(matches)

        return summary_dict

    except Exception as e:
        # Log the error and return an empty dictionary or an error message
        logger.error(f"Error executing search_data_store: {e}")
        return {}


if __name__ == "__main__":
    query = "What were Amazon's basic earnings per share (EPS) for Q4 2021, Q4 2022, the full year of 2021, and the full year of 2022?"
    company = "amazon"
    time_period = "Q4 2022"
    data_store_id = "quarterly-reports"

    results = search(query, company, time_period, data_store_id)
    summarized_ans = results['summarized_answer']
    print(summarized_ans)
    match_info = results['match_info']
    for item in match_info:
        print(item)
        print('-' * 100)
