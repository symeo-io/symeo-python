from symeo_python.configuration.config_loader import ConfigLoaderAdapter
from symeo_python.configuration.configuration import Config
from symeo_python.api_client.symeo_api_client import SymeoApiClientAdapter

config: Config = ConfigLoaderAdapter(SymeoApiClientAdapter()).load_config_from_env()
