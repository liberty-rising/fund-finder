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
                    {"terms": {"status": ["31094501", "31094502", "31094503"]}},
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
