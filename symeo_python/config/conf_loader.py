import os

import yaml

from symeo_python.config.config import Config

SYMEO_API_KEY = "SYMEO_API_KEY"
SYMEO_LOCAL_FILE = "SYMEO_LOCAL_FILE"


class ConfLoaderPort:
    def load_conf_from_env(self) -> Config:
        pass


class ConfLoaderAdapter(ConfLoaderPort):

    __conf: Config = None

    def load_conf_from_env(self) -> Config:
        if self.__conf is not None:
            return self.__conf
        if SYMEO_API_KEY in os.environ:
            pass
        elif SYMEO_LOCAL_FILE in os.environ:
            with open(os.getenv(SYMEO_LOCAL_FILE), "r") as yaml_file:
                yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                conf = Config(yaml_data)
                self.__conf = conf
                return conf
        else:
            raise Exception(
                f"Failed to load Symeo configuration due to missing api key or local configuration values file"
            )
