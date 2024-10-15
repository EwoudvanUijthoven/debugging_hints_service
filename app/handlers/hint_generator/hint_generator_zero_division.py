"""Generates hints for zero division errors."""
from typing import Union
from app.handlers.hint_generator.hint_generator_template import HintGenerator


# Function to find the parent of a given element
def find_parent(root, child):
    for elem in root.iter():
        for subelem in elem:
            if subelem == child:
                return elem
    return None


class ZeroDivisionHintGenerator(HintGenerator):
    """Generates hints for zero division errors."""

    def generate_hint(self) -> str:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Error: You have a ZeroDivison error in you code. Here is some hints to resolve the "
                                "issue:\n")
        location_hint_message = self.generate_location_hint(error_info=error_info)
        transformation_hint_message = self.generate_transformation_hint()
        behavior_hint_message = self.generate_behavior_hint()
        example_hint_message = self.generate_example_hint()
        return general_hint_message + "\n" + location_hint_message + "\n" + transformation_hint_message + "\n" + behavior_hint_message + "\n" + example_hint_message

    def gather_error_info(self) -> Union[dict, None]:
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
        return ("Transformation hint: You should transform the division operation such that no division by zero can "
                "happen. Sometimes a variable is used in a division operation and the variable is changed such that "
                "it equals 0 in some runs.\n"
        )

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return ("Behavior hint: Think about your code and division operation. When then program is running, "
                "can the denominator be 0 in the division operation?\n")

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
        return ("Example hint: When making a division operation, you cannot divide by 0. Make sure the variable which "
                "you are dividing by is not equal to 0. You can put a check in place to make sure x is never 0 when a "
                "division variable is equal to 0. For example:\n x = 0 \n if (x == "
                "0):\n \tx = 1\n print(10 / x) \n")
