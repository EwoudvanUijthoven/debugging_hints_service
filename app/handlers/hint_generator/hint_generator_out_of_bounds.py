"""Generates hints for out of bounds / index errors."""
import xml.etree.ElementTree as ET

from app.handlers.hint_generator.hint_generator_template import HintGenerator
from app.handlers.utils.helper_functions import find_parent_with_type


class OutOfBoundsHintGenerator(HintGenerator):
    """Generates hints for out of bounds / index errors."""

    def generate_hint(self) -> tuple[str, int]:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Error: You have a OutOfBounds / Index error in you code. Here is some hints to "
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
        return ("Transformation hint: You should transform the code such that when an index of a list or a string "
                "value is trying to be accessed, it is always available.\n"
                )

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return ("Behavior hint: Think about your code and accessing indexes. When then program is running, "
                "is it trying to access indexes that do not exist?\n")

    @staticmethod
    def generate_location_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        if error_info["error_statement"].startswith("if"):
            parent = "If"
        elif error_info["error_statement"].startswith("print"):
            parent = "Print"
        elif error_info["error_statement"].startswith("math.sqrt"):
            parent = "Square root"
        else:
            parent = None
        if parent:
            return f"Location hint: The possible issue is in block '{parent}' and with operation '{error_info['error_statement']}'.\n"
        else:
            return f"Location hint: The possible issue is with operation '{error_info['error_statement']}'.\n"

    @staticmethod
    def generate_example_hint() -> str:
        """Generate an example hint based on the error."""
        return ("Example hint: When accessing an index, you cannot access an index that does not exist. You can put a "
                "check in place to make sure the index exists before accessing it. For example:\nx = 'Hello World!' "
                "\nif len(x) > 7:\n\tprint(x[7])\nelse:\n\tprint('The index you are trying to access does not "
                "exist!')\n")
