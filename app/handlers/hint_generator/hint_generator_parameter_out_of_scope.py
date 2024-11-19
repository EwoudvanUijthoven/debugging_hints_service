"""Generates hints for parameter out of scope errors."""
import xml.etree.ElementTree as ET

from app.handlers.hint_generator.hint_generator_template import HintGenerator


class ParameterOutOfScopeHintGenerator(HintGenerator):
    """Generates hints for parameter out of scope errors."""

    def generate_hint(self) -> tuple[str, int]:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Warning: You are using parameters out of scope in your code. This might be undesired "
                                "and can cause your code to behave wrongly. Here is some hints to resolve the "
                                "potential issue:\n")
        location_hint_message = self.generate_location_hint(error_info=error_info)
        transformation_hint_message = self.generate_transformation_hint()
        behavior_hint_message = self.generate_behavior_hint()
        return general_hint_message + "\n" + location_hint_message + "\n" + transformation_hint_message + "\n" + behavior_hint_message, 200

    def gather_error_info(self) -> dict:
        """Gather information about the error."""
        root = ET.fromstring(self.code)
        ns = {'ns': 'http://www.w3.org/1999/xhtml'}
        error_info = {
            "function_name": None,
            "parameter_name": None,
        }
        # Find all function definitions
        function_blocks_without_return = root.findall('.//ns:block[@type="procedures_defnoreturn"]', ns)
        function_blocks_with_return = root.findall('.//ns:block[@type="procedures_defreturn"]', ns)
        function_blocks = function_blocks_without_return + function_blocks_with_return
        for block in function_blocks:
            function_name_element = block.find('.//ns:field[@name="NAME"]', ns)
            if function_name_element is not None:
                error_info["function_name"] = function_name_element.text
            parameter_blocks = block.findall('.//ns:mutation/ns:arg', ns)
            for parameter_block in parameter_blocks:
                parameter_name = parameter_block.get('name')
                # Check if the parameter is used out of scope of the function
                variable_usage = root.findall(f'.//ns:block/ns:field[@name="VAR"]', ns)
                variable_usage_in_block = block.findall(f'.//ns:block/ns:field[@name="VAR"]', ns)
                parameter_usage = [u for u in variable_usage if u.text == parameter_name]
                parameter_usage_in_block = [u for u in variable_usage_in_block if u.text == parameter_name]
                if len(parameter_usage) == 0:
                    pass
                if len(parameter_usage) > len(parameter_usage_in_block):
                    error_info["parameter_name"] = parameter_name
        return error_info

    @staticmethod
    def generate_transformation_hint() -> str:
        """Generate a transformation hint based on the error."""
        return ("To fix this issue, you need to ensure that the parameter is only used within the scope of the "
                "function. Find the usages of the parameter outside of the scope of the function and make sure they "
                "are removed or replaced with a different variable.")

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return ("Function parameters are supposed to be used only within the scope of the function. Using them "
                "outside of the function can lead to unexpected behavior in your code. Ensure that each parameter is "
                "used only within the function definition to avoid confusion and potential bugs.")

    @staticmethod
    def generate_location_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        return (f"The parameter '{error_info.get('parameter_name')}' is used outside of the function "
                f"'{error_info.get('function_name')}'. Make sure to use the parameter only within the function "
                f"definition.")
