from typing import Optional


class CliAdapter:
    def parse_conf_file_and_load_configuration(
        self, api_key: Optional[str], config_contract: str, config_file: str
    ):
        pass


class DefaultCliAdapter(CliAdapter):
    pass
