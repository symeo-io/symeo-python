from symeo_python.api_client.symeo_api_client import SymeoApiClientAdapter
from symeo_python.cli.cli import DefaultCliAdapter
from symeo_python.cli.process_runner import ProcessRunnerAdapter
from symeo_python.cli.symeo_python_cli import SymeoPythonCli
from symeo_python.configuration.config_parser import ConfigParserAdapter
from symeo_python.configuration.config_validator import ConfigValidatorAdapter
from symeo_python.yaml_converter.yaml_to_class_converter import YamlToClassAdapter

cli = SymeoPythonCli(
    DefaultCliAdapter(ConfigParserAdapter(YamlToClassAdapter()), ConfigValidatorAdapter(SymeoApiClientAdapter()), ProcessRunnerAdapter())
).load_commands()

if __name__ == "__main__":
    cli()
