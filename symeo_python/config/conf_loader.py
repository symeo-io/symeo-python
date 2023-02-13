import os

import yaml

from symeo_python.config.config import Config
from symeo_python.config.symeo_api_client import SymeoApiClientPort

SYMEO_API_KEY = "SYMEO_API_KEY"
SYMEO_LOCAL_FILE = "SYMEO_LOCAL_FILE"


class ConfLoaderPort:
    def load_conf_from_env(self) -> Config:
        pass


class ConfLoaderAdapter(ConfLoaderPort):
    def __init__(self, symeo_api_client_port: SymeoApiClientPort):
        self.__symeo_api_client_port = symeo_api_client_port

    __conf: Config = None

    def load_conf_from_env(self) -> Config:
        if self.__conf is not None:
            return self.__conf
        if SYMEO_API_KEY in os.environ:
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
            conf = Config(yaml_data)
            self.__conf = conf
            return conf

    def __fetch_configuration_values_from_symeo_api(self):
        yaml_data = self.__symeo_api_client_port.get_conf_values_for_api_key(
            os.getenv(SYMEO_API_KEY)
        )
        conf = Config(yaml_data)
        self.__conf = conf
        return conf
