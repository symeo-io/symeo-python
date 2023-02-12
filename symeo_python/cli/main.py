import os

from symeo_python.cli.cli_adapter import DefaultCliAdapter
from symeo_python.cli.symeo_python_cli import SymeoPythonCli
from symeo_python.yaml.yaml_to_class_converter import YamlToClassAdapter

cli = SymeoPythonCli(DefaultCliAdapter(YamlToClassAdapter())).load_commands()

if __name__ == "__main__":
    cli()
