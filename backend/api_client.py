import requests
import json


class EUFundingAPIClient:
    BASE_URL = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"
    API_KEY = "SEDIA"

    def __init__(self):
        self.session = requests.Session()

    def get_grants_and_tenders(self):
        query = {
            "bool": {
                "must": [
                    {"terms": {"type": ["0", "1", "2", "8"]}},
                    {"terms": {"status": ["31094501", "31094502"]}},
                    {"terms": {"language": ["en"]}},
                ]
            }
        }
        return self._make_request(query)

    def _make_request(self, query):
        response = self.session.post(
            f"{self.BASE_URL}?apiKey={self.API_KEY}&text=***",
            data={"query": json.dumps(query)},
        )
        response.raise_for_status()
        return response.json()

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
