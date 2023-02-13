from symeo_python.config.config import Config
from symeo_python.config.conf_loader import ConfLoaderAdapter

config: Config = ConfLoaderAdapter().load_conf_from_env()