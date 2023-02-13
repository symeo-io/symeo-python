from symeo_python.config.conf_loader import ConfLoaderAdapter
from symeo_python.config.config import Config
from symeo_python.config.symeo_api_client import SymeoApiClientAdapter

config: Config = ConfLoaderAdapter(SymeoApiClientAdapter()).load_conf_from_env()
