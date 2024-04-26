from google.cloud import discoveryengine_v1beta as discoveryengine
from google.api_core.client_options import ClientOptions
from google.protobuf import json_format
from src.config.logging import logger 
from src.config.setup import config
from typing import Optional
from typing import Dict
from typing import List
from typing import Any


LOCATION = "global" 


def search_data_store(search_query: str, data_store_id: str) -> Optional[discoveryengine.SearchResponse]:
    """
    Searches the data store using Google Cloud's Discovery Engine API.

    Args:
        search_query (str): The search query string.
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


def extract_relevant_data(response: Optional[discoveryengine.SearchResponse]) -> List[Dict[str, Any]]:
    """
    Extracts title, snippet, and link from the search response.

    Args:
        response (Optional[discoveryengine.SearchResponse]): The search response object from the Discovery Engine API.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the extracted information.
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
            "id": "",
            "title": "",
            "link": "",
            "company": "",
            "time_period": "",
            "extractive_answers": [],
            "extractive_segments": []
        }

        # Convert protocol buffer message to JSON
        result_json = json_format.MessageToDict(result.document._pb)

        # Extracting fields from JSON
        struct_data = result_json.get('structData', {})
        derived_struct_data = result_json.get('derivedStructData', {})

        id = result_json['id']
        data['id'] = id

        title = derived_struct_data['title']
        data['title'] = title

        company = struct_data['company']
        data['company'] = company

        time_period = struct_data['time_period']
        data['time_period'] = time_period

        # Collect extractive answers 
        extractive_answers = derived_struct_data.get("extractive_answers", [])
        answers = [answer["content"] for answer in extractive_answers]
        data['extractive_answers'] = answers

        # Collect extractive segments
        extractive_segments = derived_struct_data.get("extractive_segments", [])
        segments = [segment["content"] for segment in extractive_segments]
        data["extractive_segments"] = segments

        # Extracting link
        link = derived_struct_data.get("link")
        if link:
            data["link"] = link

        extracted_data.append(data)
    return extracted_data


def create_summary_dict(matches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Creates a dictionary with the relevant data extracted from the matches.

    Args:
        matches (List[Dict[str, Any]]): List of match data extracted.

    Returns:
        Dict[str, Any]: A dictionary containing the summary and details of each match.
    """
    summary_dict = {"summarized_answer": matches[0]}
    match_info = []

    rank = 1
    for match in matches[1:]:
        info = {
            "rank": rank,
            "id": match["id"],
            "title": match["title"],
            "link": match["link"],
            "company": match["company"],
            "time_period": match["time_period"],
            "extractive_answers": match["extractive_answers"],
            "extractive_segments": match["extractive_segments"]
        }
        match_info.append(info)
        rank += 1

    summary_dict["match_info"] = match_info

    return summary_dict