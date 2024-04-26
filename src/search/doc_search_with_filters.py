from src.search.utils import filtered_search
from src.config.logging import logger 


if __name__ == "__main__":
    query = "What were Amazon's basic earnings per share (EPS) for Q4 2021, Q4 2022, the full year of 2021, and the full year of 2022?"
    company = "amazon"
    time_period = "Q4 2022"
    data_store_id = "quarterly-reports"

    results = filtered_search(query, company, time_period, data_store_id)
    summarized_ans = results['summarized_answer']
    print(summarized_ans)
    match_info = results['match_info']
    for item in match_info:
        print(item)
        print('-' * 100)
