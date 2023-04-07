import os
import re
from typing import List

import yaml

from symeo_python.api_client.symeo_api_client import SymeoApiClientPort
from symeo_python.configuration.config_loader import SYMEO_API_KEY, SYMEO_LOCAL_FILE, SYMEO_API_URL


class ConfigValidatorPort:
    def validate_config_from_env(self, config_contract: str) -> List[str]:
        pass


class ConfigValidatorAdapter(ConfigValidatorPort):
    def __init__(self, symeo_api_client_port: SymeoApiClientPort):
        self.__symeo_api_client_port = symeo_api_client_port

    def validate_config_from_env(self, config_contract: str) -> List[str]:
        if SYMEO_API_KEY in os.environ and SYMEO_API_URL in os.environ:
            errors: List[str] = self.__validate_configuration_values_from_symeo_api(config_contract)
        elif SYMEO_LOCAL_FILE in os.environ:
            errors: List[str] = self.__validate_yaml_values(config_contract)
        else:
            raise Exception(
                "Failed to validate configuration due to missing api key or local configuration values file"
            )
        return errors

    def __validate_configuration_values_from_symeo_api(self, config_contract: str) -> List[str]:
        with open(config_contract, "r") as yaml_contract:
            contract = yaml.load(yaml_contract, Loader=yaml.FullLoader)
        values = self.__symeo_api_client_port.get_conf_values_for_api_key(os.getenv(SYMEO_API_URL),
                                                                          os.getenv(SYMEO_API_KEY))
        return self.__check_contract_type_compatibility(contract, values)

    def __validate_yaml_values(self, config_contract: str) -> List[str]:
        with open(config_contract, "r") as yaml_contract:
            contract = yaml.load(yaml_contract, Loader=yaml.FullLoader)
        with open(os.getenv(SYMEO_LOCAL_FILE)) as yaml_values:
            values = yaml.load(yaml_values, Loader=yaml.FullLoader)
        return self.__check_contract_type_compatibility(contract, values)

    def __check_contract_type_compatibility(self, contract: dict, values: dict, parent_path: str = None):
        errors = []
        for property_name in contract.keys():
            contract_property = contract.get(property_name)
            values_property = values.get(property_name)

            if not self.__is_contract_property(contract_property) and self.__is_undefined(values_property):
                errors.append(self.__build_missing_property_error(property_name, parent_path))
                continue

            if not self.__is_contract_property(contract_property) and self.__is_defined(values_property):
                errors += self.__check_contract_type_compatibility(contract_property, values_property,
                                                                   self.__build_parent_path(parent_path, property_name))
                continue

            if not self.__is_contract_property_optional(contract_property) and self.__is_undefined(values_property):
                errors.append(self.__build_missing_property_error(property_name, parent_path))
                continue

            if self.__is_defined(values_property) and not self.__contract_property_and_value_have_same_type(
                    contract_property, values_property):
                errors.append(
                    self.__build_wrong_type_error(property_name, parent_path, contract_property, values_property))
                continue
            if self.__is_defined(values_property) and self.__has_regex(
                    contract_property) and not self.__value_match_contract_regex(contract_property, values_property):
                errors.append(
                    self.__build_wrong_regex_error(property_name, parent_path, contract_property, values_property))
        return errors

    @staticmethod
    def __is_contract_property(contract_property: dict):
        return contract_property.get('type')

    def __is_undefined(self, values_property: dict) -> bool:
        return not self.__is_defined(values_property)

    @staticmethod
    def __is_defined(values_property: dict) -> bool:
        return (values_property is not None) and (values_property != '')

    @staticmethod
    def __is_contract_property_optional(contract_property: dict) -> bool:
        optional = contract_property.get("optional")
        return True if optional else False

    @staticmethod
    def __contract_property_and_value_have_same_type(contract_property: dict, values_property) -> bool:
        contract_property_type = contract_property.get("type")
        if contract_property_type == "string" and type(values_property) == str:
            return True
        if contract_property_type == "integer" and type(values_property) == int:
            return True
        if contract_property_type == "float" and type(values_property) == float:
            return True
        if contract_property_type == "boolean" and type(values_property) == bool:
            return True
        return False

    @staticmethod
    def __has_regex(contract_property) -> bool:
        return contract_property.get("regex") is not None

    @staticmethod
    def __value_match_contract_regex(contract_property, values_property):
        return contract_property.get("regex") is not None and re.search(contract_property.get("regex"), values_property)

    def __build_missing_property_error(self, property_name, parent_path) -> str:
        displayed_property_name = self.__build_parent_path(parent_path, property_name)
        return f'The property [bold white]"{displayed_property_name}"[/bold white] of your configuration contract [bold red]is missing[/bold red] in your configuration values.'

    @staticmethod
    def __build_parent_path(previous_parent_path: str, property_name: str) -> str:
        return property_name if previous_parent_path is None else f'{previous_parent_path}.{property_name}'

    def __build_wrong_type_error(self, property_name: str, parent_path: str, contract_property: dict,
                                 values_property) -> str:
        displayed_property_name = self.__build_parent_path(parent_path, property_name)
        return f'Configuration property [bold white]"{displayed_property_name}"[/bold white] has type [bold red]"{type(values_property)}"[/bold red] while configuration contract defined "{displayed_property_name}"' \
               f' as [bold green]"{contract_property.get("type")}"[/bold green]'

    def __build_wrong_regex_error(self, property_name, parent_path, contract_property, values_property) -> str:
        displayed_property_name = self.__build_parent_path(parent_path, property_name)
        return f'Configuration property [bold white]"{displayed_property_name}"[/bold white] with value "{values_property}" does not match regex [bold green]"{contract_property.get("regex")}"[/bold green] defined in contract'
