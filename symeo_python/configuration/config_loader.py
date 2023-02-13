import os

import yaml

from symeo_python.api_client.symeo_api_client import SymeoApiClientPort
from symeo_python.configuration.configuration import Config

SYMEO_API_KEY = "SYMEO_API_KEY"
SYMEO_API_URL = "SYMEO_API_URL"
SYMEO_LOCAL_FILE = "SYMEO_LOCAL_FILE"


class ConfigLoaderPort:
    def load_config_from_env(self) -> Config:
        pass


class ConfigLoaderAdapter(ConfigLoaderPort):
    def __init__(self, symeo_api_client_port: SymeoApiClientPort):
        self.__symeo_api_client_port = symeo_api_client_port

    __config: Config = None

    def load_config_from_env(self) -> Config:
        if self.__config is not None:
            return self.__config
        if SYMEO_API_KEY in os.environ and SYMEO_API_URL in os.environ:
            return self.__fetch_configuration_values_from_symeo_api()
        elif SYMEO_LOCAL_FILE in os.environ:
            return self.__load_yaml_values()
        else:
            raise Exception(
                f"Failed to load Symeo configuration due to missing api key or local configuration values file"
            )

    def __load_yaml_values(self):
        with open(os.getenv(SYMEO_LOCAL_FILE), "r") as yaml_file:
            yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            config = Config(yaml_data)
            self.__config = config
            return config

    def __fetch_configuration_values_from_symeo_api(self):
        yaml_data = self.__symeo_api_client_port.get_conf_values_for_api_key(
            os.getenv(SYMEO_API_URL), os.getenv(SYMEO_API_KEY)
        )
        config = Config(yaml_data)
        self.__config = config
        return config
