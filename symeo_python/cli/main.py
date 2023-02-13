from symeo_python.cli.cli import DefaultCliAdapter
from symeo_python.cli.process_runner import ProcessRunnerAdapter
from symeo_python.cli.symeo_python_cli import SymeoPythonCli
from symeo_python.config.conf_parser import ConfParserAdapter
from symeo_python.yaml_converter.yaml_to_class_converter import YamlToClassAdapter

cli = SymeoPythonCli(
    DefaultCliAdapter(ConfParserAdapter(YamlToClassAdapter()), ProcessRunnerAdapter())
).load_commands()

if __name__ == "__main__":
    cli()
