import requests

SYMEO_API_KEY_HEADER = "X-API-KEY"
# SYMEO_API_URL = "https://api.symeo.io/api/v1/values"
SYMEO_API_URL = "https://config-staging.symeo.io/api/v1/values"


class SymeoApiClientPort:
    def get_conf_values_for_api_key(self, api_key) -> dict:
        pass


class SymeoApiClientAdapter(SymeoApiClientPort):
    def get_conf_values_for_api_key(self, api_key):
        response = requests.get(
            url=SYMEO_API_URL, headers={SYMEO_API_KEY_HEADER: api_key}
        )
        if response.status_code != 200:
            raise Exception(
                f"Http status {response.status_code} - Failed to fetch configuration values from Symeo API {SYMEO_API_URL}"
            )
        return response.json()
