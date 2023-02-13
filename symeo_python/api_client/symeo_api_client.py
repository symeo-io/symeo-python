import requests

SYMEO_API_KEY_HEADER = "X-API-KEY"


class SymeoApiClientPort:
    def get_conf_values_for_api_key(self, api_url: str, api_key: str) -> dict:
        pass


class SymeoApiClientAdapter(SymeoApiClientPort):
    def get_conf_values_for_api_key(self, api_url, api_key):
        response = requests.get(url=api_url, headers={SYMEO_API_KEY_HEADER: api_key})
        if response.status_code != 200:
            raise Exception(
                f"Http status {response.status_code} - Failed to fetch configuration values from Symeo API {api_url}"
            )
        return response.json()["values"]
