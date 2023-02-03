import shutil
import tempfile
import unittest
from hashlib import md5  # type: ignore
from mmap import ACCESS_READ, mmap  # type: ignore

from symeo_python.yaml.yaml_to_class_converter import YamlToClassConverter


class YamlToClassConverterTest(unittest.TestCase):

    __temp_dir: str

    def setUp(self) -> None:
        self.__temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.__temp_dir)

    def test_should_convert_simple_yaml_files(self):
        self.__assert_generated_python_file_equals_expected_python_file(
            "simple_yaml_1.yml", "simple_yaml_1.py"
        )
        self.__assert_generated_python_file_equals_expected_python_file(
            "simple_yaml_2.yml", "simple_yaml_2.py"
        )
        self.__assert_generated_python_file_equals_expected_python_file(
            "simple_yaml_with_two_attributes.yml", "simple_yaml_with_two_attributes.py"
        )

    def test_should_convert_complex_yaml_files(self):
        self.__assert_generated_python_file_equals_expected_python_file(
            "yaml_with_nested_conf.yml", "yaml_with_nested_conf.py"
        )

    def test_should_convert_complex_name(self):
        self.__assert_generated_python_file_equals_expected_python_file(
            "yaml_with_complex_name.yml", "yaml_with_complex_name.py"
        )
        self.__assert_generated_python_file_equals_expected_python_file(
            "complex_yaml_with_complex_class_name.yml",
            "complex_yaml_with_complex_class_name.py",
        )

    def __assert_generated_python_file_equals_expected_python_file(
        self, yaml_file_name, python_file_name
    ):
        given_yaml_file = "resources/given_yaml_files/%s" % yaml_file_name
        expected_python_file = "resources/expected_python_files/%s" % python_file_name
        target_path = f"{self.__temp_dir}/%s" % python_file_name
        yaml_to_class_converter = YamlToClassConverter(target_path)

        # When
        yaml_to_class_converter.parse_configuration_from_path(given_yaml_file)

        # Then
        self.assertEqual(
            self.__get_file_md5(expected_python_file), self.__get_file_md5(target_path)
        )

    def __get_file_md5(self, file_path) -> str:
        with open(file_path) as file, mmap(  # type: ignore
            file.fileno(), 0, access=ACCESS_READ
        ) as file:
            return md5(file).hexdigest()  # type: ignore
