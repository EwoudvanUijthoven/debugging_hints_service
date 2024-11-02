"""Generates hints for type errors."""
import xml.etree.ElementTree as ET

from app.handlers.hint_generator.hint_generator_template import HintGenerator
from app.handlers.utils.helper_functions import check_variable_type


class TypeErrorHintGenerator(HintGenerator):
    """Generates hints for type errors."""

    def generate_hint(self) -> tuple[str, int]:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Warning: You are having a type error in your code. Here is some hints to "
                                "resolve the issue:\n")
        location_hint_message = self.generate_location_hint(error_info=error_info)
        data_hint_message = self.generate_data_hint(error_info=error_info)
        transformation_hint_message = self.generate_transformation_hint()
        behavior_hint_message = self.generate_behavior_hint()
        example_hint_message = self.generate_example_hint()
        return general_hint_message + "\n" + location_hint_message + "\n" + data_hint_message + "\n" + transformation_hint_message + "\n" + behavior_hint_message + "\n" + example_hint_message, 200

    def gather_error_info(self) -> dict:
        """Gather information about the error."""
        root = ET.fromstring(self.code)
        error_info = {
            "a_type": None,
            "b_type": None,
            "a_value": None,
            "b_value": None,
        }
        ns = {'ns': 'http://www.w3.org/1999/xhtml'}
        # Find all the blocks that have math in there
        math_blocks = root.findall('.//ns:block[@type="math_arithmetic"]', ns)
        for block in math_blocks:
            # Comparison values
            value_a_block = block.find('.//ns:value[@name="A"]/ns:block', ns)
            value_b_block = block.find('.//ns:value[@name="B"]/ns:block', ns)
            type_a = value_a_block.get("type")
            type_b = value_b_block.get("type")
            # Comparing 2 string values
            if type_a == "variables_get":
                variable_name_a = value_a_block.find('.//ns:field', ns).text
                type_a = check_variable_type(variable_name_a, root, ns)
            if type_b == "variables_get":
                variable_name_b = value_b_block.find('.//ns:field', ns).text
                type_b = check_variable_type(variable_name_b, root, ns)
            if type_a != type_b:
                error_info["a_type"] = type_a
                error_info["b_type"] = type_b
                error_info["a_value"] = value_a_block.find('.//ns:field', ns).text
                error_info["b_value"] = value_b_block.find('.//ns:field', ns).text
                return error_info
        raise NotImplementedError("No supported type error found.")

    @staticmethod
    def generate_transformation_hint() -> str:
        """Generate a transformation hint based on the error."""
        return ("Transformation hint: You should transform the code such that the types of the variables being "
                "compared are equal.\n")

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return ("Behavior hint: Think about your code and the types of the variables being compared. When applying "
                "operations on multiple variables they should have the same type.\n")

    @staticmethod
    def generate_data_hint(error_info: dict) -> str:
        """Generate a data hint based on the error."""
        a_type = error_info.get("a_type")
        b_type = error_info.get("b_type")
        a_value = error_info.get("a_value")
        b_value = error_info.get("b_value")
        return (
            f"Data hint: The variable '{a_value}' is of type '{a_type}', while the variable '{b_value}' is of type "
            f"'{b_type}'. Ensure that both variables are of the same type before performing operations on them.\n")

    @staticmethod
    def generate_location_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        a_value = error_info.get("a_value")
        b_value = error_info.get("b_value")
        return (f"Location hint: The type error occurred when trying to perform an operation between '{a_value}' "
                f"and '{b_value}'. Check the location in your code where these variables are used together.\n")

    @staticmethod
    def generate_example_hint() -> str:
        """Generate an example hint based on the error."""
        return ("Example hint: If you are trying to add an integer and a string, you should convert the string to an "
                "integer first. For example, instead of `result = 5 + '10'`, use `result = 5 + int('10')`.\n")
