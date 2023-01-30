import os


class ConfigurationParser:

    __SUPPORTED_EXTENSIONS__ = [".yml", ".yaml"]

    def load_configuration(self, configuration_path: str):
        if os.path.isfile(configuration_path) is False:
            raise Exception(f"Configuration file {configuration_path} not found")
        else:
            if self.validate_file_extension(configuration_path):
                pass
            else:
                raise Exception(
                    f"Wrong configuration file format for {configuration_path} . Only .yml and .yaml are accepted"
                )

    def validate_file_extension(self, configuration_path):
        is_file_extension_supported = False
        for supported_extension in self.__SUPPORTED_EXTENSIONS__:
            if configuration_path.endswith(supported_extension):
                is_file_extension_supported = True
        return is_file_extension_supported
