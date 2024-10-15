"""Generates hints for comparing literals errors."""
import xml.etree.ElementTree as ET

from app.handlers.hint_generator.hint_generator_template import HintGenerator
from app.handlers.utils.helper_functions import find_parent_with_type


class ComparingLiteralsHintGenerator(HintGenerator):
    """Generates hints for comparing literals errors."""

    def generate_hint(self) -> str:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Warning: You are comparing literals in you code. This might be undesired and can cause"
                                " your code to behave wrongly. Here is some hints to resolve the potential issue:\n")
        location_hint_message = self.generate_location_hint(error_info=error_info)
        data_hint_message = self.generate_data_hint(error_info=error_info)
        transformation_hint_message = self.generate_transformation_hint()
        behavior_hint_message = self.generate_behavior_hint()
        example_hint_message = self.generate_example_hint()
        return general_hint_message + "\n" + location_hint_message + "\n" + data_hint_message + "\n" + transformation_hint_message + "\n" + behavior_hint_message + "\n" + example_hint_message

    def gather_error_info(self) -> dict:
        """Gather information about the error."""
        root = ET.fromstring(self.code)
        ns = {'ns': 'http://www.w3.org/1999/xhtml'}
        error_info = {
            "a_type": None,
            "b_type": None,
            "a_value": None,
            "b_value": None,
            "operator": None,
            "parent_block": None
        }
        # Find all the blocks that compare 2 objects
        logic_compare_blocks = root.findall('.//ns:block[@type="logic_compare"]', ns)
        for block in logic_compare_blocks:
            # Comparison values
            value_a_block = block.find('.//ns:value[@name="A"]/ns:block', ns)
            value_b_block = block.find('.//ns:value[@name="B"]/ns:block', ns)
            error_info["operator"] = block.find('.//ns:field[@name="OP"]', ns).text
            error_info["parent_block"] = find_parent_with_type(root, block).get('type') if not None else None
            error_info["a_value"] = value_a_block.find('.//ns:field', ns).text
            error_info["b_value"] = value_b_block.find('.//ns:field', ns).text

            # Comparing 2 string values
            if value_a_block.get("type") == "text" and value_b_block.get("type") == "text":
                error_info["a_type"] = "string"
                error_info["b_type"] = "string"
                return error_info
            # Comparing 2 number values
            elif value_a_block.get("type") == "math_number" and value_b_block.get("type") == "math_number":
                error_info["a_type"] = "number"
                error_info["b_type"] = "number"
                return error_info
            # Comparing 2 boolean values
            elif value_a_block.get("type") == "logic_boolean" and value_b_block.get("type") == "logic_boolean":
                error_info["a_type"] = "boolean"
                error_info["b_type"] = "boolean"
                return error_info

    @staticmethod
    def generate_transformation_hint() -> str:
        """Generate a transformation hint based on the error."""
        return ("Transformation hint: You should transform at least one of the literals into a variable before "
                "comparing them.\n")

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return ("Behavior hint: Think about your code and comparison. Are you comparing the right values? Currently "
                "the outcome of the comparison is the same every time the program runs.\n")

    @staticmethod
    def generate_data_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        return (f"Data hint: You are comparing {error_info['a_type']} '{error_info['a_value']}' with "
                f"{error_info['b_type']} '{error_info['b_value']}'. We are expecting variables for comparison.\n")

    @staticmethod
    def generate_location_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        operator_mapping = {
            "EQ": "=",
            "NEQ": "≠",
            "LT": "<",
            "LTE": "≤",
            "GT": ">",
            "GTE": "≥"
        }
        operator = operator_mapping[error_info["operator"]]
        parent_mapping = {
            "controls_if": "if",
            "controls_ifelse": "if-else",
            "controls_whileUntil": "repeat-while"

        }
        parent_block = parent_mapping[error_info["parent_block"]] if error_info["parent_block"] in parent_mapping else None
        if parent_block:
            return (f"Location hint: The possible issue is in block '{parent_block}' and with comparison "
                    f"'{error_info['a_value']} {operator} {error_info['b_value']}'.\n")
        else:
            return (f"Location hint: The possible issue is with comparison '{error_info['a_value']} "
                    f"{operator} {error_info['b_value']}'.\n")

    @staticmethod
    def generate_example_hint() -> str:
        """Generate an example hint based on the error."""
        return ("Example hint: When making a comparison, you usually want to compare variables. For example, "
                "if you have a variable x with value 'test', you want to check x = 'test' instead of 'test' = 'test'.\n")
