"""Generates hints for ambiguous parameter name."""
import xml.etree.ElementTree as ET

from app.handlers.hint_generator.hint_generator_template import HintGenerator


class AmbiguousParameterNameHintGenerator(HintGenerator):
    """Generates hints for ambiguous parameter names."""

    def generate_hint(self) -> tuple[str, int]:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Warning: You are have ambiguous parameter names in your code. Here is some hints to resolve the issue:\n")
        location_hint_message = self.generate_location_hint(error_info=error_info)
        data_hint_message = self.generate_data_hint(error_info=error_info)
        transformation_hint_message = self.generate_transformation_hint()
        behavior_hint_message = self.generate_behavior_hint()
        example_hint_message = self.generate_example_hint()
        return general_hint_message + "\n" + location_hint_message + "\n" + data_hint_message + "\n" + transformation_hint_message + "\n" + behavior_hint_message + "\n" + example_hint_message, 200

    def gather_error_info(self) -> dict:
        """Gather information about the error."""
        root = ET.fromstring(self.code)
        ns = {'ns': 'http://www.w3.org/1999/xhtml'}
        error_info = {
            "function_name": None,
            "ambiguous_parameter_names": None
        }
        # Find all the blocks that have ambiguous parameter names
        function_blocks_without_return = root.findall('.//ns:block[@type="procedures_defnoreturn"]', ns)
        function_blocks_with_return = root.findall('.//ns:block[@type="procedures_defreturn"]', ns)
        function_blocks = function_blocks_without_return + function_blocks_with_return

        for block in function_blocks:
            # Get the function name
            function_name = block.find('.//ns:field[@name="NAME"]', ns).text
            parameter_names = []
            # Get all the parameter names
            parameter_blocks = block.findall('.//ns:mutation/ns:arg', ns)
            for parameter_block in parameter_blocks:
                parameter_names.append(parameter_block.get('name'))
            # Check if there are any duplicate parameter names
            if len(parameter_names) != len(set(parameter_names)):
                for parameter_name in parameter_names:
                    if parameter_names.count(parameter_name) > 1:
                        error_info["function_name"] = function_name
                        error_info["ambiguous_parameter_names"] = parameter_name
                        return error_info
        raise NotImplementedError("No ambiguous parameter names found.")

    @staticmethod
    def generate_transformation_hint() -> str:
        """Generate a transformation hint based on the error."""
        return "You should rename the ambiguous parameter names in the function definition.\n"

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return ("Using ambiguous parameter names can lead to unexpected behavior in your functions. "
                "Ensure that each parameter name is unique to avoid confusion and potential bugs.\n")

    @staticmethod
    def generate_data_hint(error_info: dict) -> str:
        """Generate a data hint based on the error."""
        function_name = error_info.get("function_name")
        ambiguous_parameter_name = error_info.get("ambiguous_parameter_names")
        return (f"The function '{function_name}' has ambiguous parameter names. The parameter name "
                f"'{ambiguous_parameter_name}' is used more than once. Ensure that each parameter name is unique.\n")

    @staticmethod
    def generate_location_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        function_name = error_info.get("function_name")
        ambiguous_parameter_name = error_info.get("ambiguous_parameter_names")
        return (
            f"The function '{function_name}' has an ambiguous parameter name '{ambiguous_parameter_name}'. "
            "Check the function definition and ensure that each parameter name is unique.\n")

    @staticmethod
    def generate_example_hint() -> str:
        """Generate an example hint based on the error."""
        return (
            "If you have a function with ambiguous parameter names, rename the parameters to be unique. "
            "For example, instead of `def my_function(a, a):`, use `def my_function(a, b):`.\n")
