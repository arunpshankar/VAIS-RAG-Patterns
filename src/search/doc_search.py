from google.cloud import discoveryengine_v1beta as discoveryengine
from google.api_core.client_options import ClientOptions
from google.protobuf import json_format
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
        data_store_d (str): Vertex AI Search Data Store ID.

    Returns:
        discoveryengine.SearchResponse: The search response from the Discovery Engine API.
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


def extract_relevant_data(response: Optional[discoveryengine.SearchResponse]):
    """
    Extracts company, title, snippet, and link from the search response.

    Args:
        response (discoveryengine.SearchResponse): The search response object from the Discovery Engine API.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the extracted information.
    """
    extracted_data = []

    if response is None:
        logger.error("No response received to extract data.")
        return extracted_data
    
    summary = response.summary.summary_text
    if summary:
        extracted_data.append(summary)
        
    for result in response.results:
        data = {
            "extractive_answers": [],
            "extractive_segments": [],
            "knol_id": "",
            "link": ""
        }

        # Convert protocol buffer message to JSON
        result_json = json_format.MessageToDict(result.document._pb)

        # Extracting fields from JSON
        struct_data = result_json.get('structData', {})
        derived_struct_data = result_json.get('derivedStructData', {})

        knol_id = struct_data.get("Id")
        data['knol_id'] = knol_id

        # Collect extractive answers 
        extractive_answers = derived_struct_data.get("extractive_answers")
        if extractive_answers:
            answers = []
            for answer in extractive_answers:
                answers.append(answer["content"])
        data['extractive_answers'] = answers

        # Collect extractive segmentss
        extractive_segments = derived_struct_data.get("extractive_segments")
        if extractive_segments:
            segments = []
            for segment in extractive_segments:
                segments.append(segment["content"])
            data["extractive_segments"] = segments

        # Extracting link
        link = derived_struct_data.get("link")
        if link:
            data["link"] = link

        extracted_data.append(data)
    return extracted_data


def create_summary_dict(matches):
    """
    Create a dictionary with the relevant data extracted from the matches.

    :param matches: List of match data extracted.
    :return: A dictionary containing the summary and details of each match.
    """
    summary_dict = {"summarized_answer": matches[0]}
    match_info = []

    rank = 1
    for match in matches[1:]:
        info = {
            "rank": rank,
            "link": match["link"],
            "knowledge_id": match["knol_id"][0],
            "extractive_answers": match["extractive_answers"],
            "extractive_segments": match["extractive_segments"]
        }
        match_info.append(info)
        rank += 1

    summary_dict["match_info"] = match_info

    return summary_dict


def search(query: str, brand: str, data_store_id: str) -> Dict[str, Any]:
    """
    Searches a data store based on a given search query and brand, 
    then consolidates the results in a dictionary.

    Parameters:
    query (str): The query used for searching the data store.
    brand (str): The brand to filter the search results.
    data_store_id (str): Vertex AI Search Data Store ID.

    Returns:
    Dict[str, Any]: A dictionary containing the consolidated results of the search.
                    Returns an empty dictionary if an error occurs.
    """
    filter_str = f"Brand: ANY(\"{brand}\")"

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
    query = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    brand = "Alphabet"
    data_store_id = "quarterly-reports"

    result = search(query, brand, data_store_id)
    print(result)