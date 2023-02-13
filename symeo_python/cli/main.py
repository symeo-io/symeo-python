from symeo_python.cli.cli_adapter import DefaultCliAdapter
from symeo_python.cli.symeo_python_cli import SymeoPythonCli
from symeo_python.config.conf_loader import ConfLoaderAdapter
from symeo_python.config.conf_parser import ConfParserAdapter
from symeo_python.yaml.yaml_to_class_converter import YamlToClassAdapter

cli = SymeoPythonCli(
    DefaultCliAdapter(ConfParserAdapter(YamlToClassAdapter()), ConfLoaderAdapter())
).load_commands()

if __name__ == "__main__":
    cli()
