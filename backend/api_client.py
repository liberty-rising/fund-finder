import requests
import json
import os


class EUFundingAPIClient:
    BASE_URL = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"
    API_KEY = "SEDIA"
    QUERY_FILE_PATH = "euft_search_query.json"

    def __init__(self):
        self.session = requests.Session()

    def _make_request(self, page_number, page_size):
        # Read the entire JSON file content
        with open(self.QUERY_FILE_PATH, "r") as query_file:
            query_content = query_file.read()

        # Prepare the files parameter
        files = {"query": ("query.json", query_content, "application/json")}

        # Prepare other form data
        data = {"pageSize": str(page_size), "pageNumber": str(page_number)}

        response = self.session.post(
            f"{self.BASE_URL}?apiKey={self.API_KEY}&text=***", files=files, data=data
        )
        response.raise_for_status()
        return response.json()

    def get_grants_and_tenders(self, page_number=1, page_size=100):
        return self._make_request(page_number, page_size)

    # Type definitions:
    # "0": "Tender"
    # "1": "Grant"
    # "2": "Calls for proposals"
    # "6": "Funding updates"
    # "8": "Cascade funding calls"
    # "11": Unknown

    # Status definitions:
    # "31094501": "Forthcoming"
    # "31094502": "Open for submission"
    # "31094503": "Closed"
    # "Cancelled after publication": "Cancelled after publication"
    # "99999998": Unknown

    # Note: The current query fetches types 0, 1, 2, and 8 (Tenders, Grants, Calls for proposals, and Cascade funding calls)
    # with statuses 31094501, 31094502 (Forthcoming, Open for submission)
