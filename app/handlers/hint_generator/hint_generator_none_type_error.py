"""Generates hints for none type errors."""
import xml.etree.ElementTree as ET

from app.handlers.hint_generator.hint_generator_template import HintGenerator
from app.handlers.utils.helper_functions import check_variable_type


class NoneTypeHintGenerator(HintGenerator):
    """Generates hints for none type errors."""

    def generate_hint(self) -> tuple[str, int]:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Warning: You are having a none type error in your code. Here is some hints to "
                                "resolve the issue:\n")
        location_hint_message = self.generate_location_hint(error_info=error_info)
        transformation_hint_message = self.generate_transformation_hint()
        behavior_hint_message = self.generate_behavior_hint()
        example_hint_message = self.generate_example_hint()
        return general_hint_message + "\n" + location_hint_message + "\n" + transformation_hint_message + "\n" + behavior_hint_message + "\n" + example_hint_message, 200

    def gather_error_info(self) -> dict:
        """Gather information about the error."""
        error_info = {
            "error_statement": None,
        }
        error_lines = self.error.strip().split("\n")
        error_variables = error_lines[-2].strip()
        error_info["error_statement"] = error_variables
        return error_info

    @staticmethod
    def generate_transformation_hint() -> str:
        """Generate a transformation hint based on the error."""
        return "You should make sure that the variables are assigned a value before using operations on them.\n"

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return "Using variables that are not assigned a value can lead to unexpected behavior in your code.\n"

    @staticmethod
    def generate_location_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        return (f"The possible issue is with operation '{error_info['error_statement']}'. Find the operation in your "
                f"blocks.\n")

    @staticmethod
    def generate_example_hint() -> str:
        """Generate an example hint based on the error."""
        return ("An example of preventing a non type error is to ensure that the variables are assigned a value "
                "before using them. So if we have a variable a and we want to do operation a + 1, we should make sure "
                "that a is assigned a value by saying a = 0 before using it in the operation.\n")
