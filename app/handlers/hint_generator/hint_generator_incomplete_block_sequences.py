"""Generates hints for incomplete block sequences."""
import xml.etree.ElementTree as ET

from app.handlers.hint_generator.hint_generator_template import HintGenerator


class IncompleteBlockSequencesGenerator(HintGenerator):
    """Generates hints for incomplete block sequences."""

    def generate_hint(self) -> tuple[str, int]:
        """Generate a hint based on the error."""
        error_info = self.gather_error_info()
        general_hint_message = ("Warning: You are having incomplete block sequences in you code. This might be undesired and can cause"
                                " your code to behave wrongly. Here is some hints to resolve the potential issue:\n")
        location_hint_message = self.generate_location_hint(error_info=error_info)
        transformation_hint_message = self.generate_transformation_hint()
        behavior_hint_message = self.generate_behavior_hint()
        example_hint_message = self.generate_example_hint()
        return general_hint_message + "\n" + location_hint_message + "\n" + transformation_hint_message + "\n" + behavior_hint_message + "\n" + example_hint_message, 200

    def gather_error_info(self) -> dict:
        """Gather information about the error."""
        root = ET.fromstring(self.code)
        ns = {'ns': 'http://www.w3.org/1999/xhtml'}
        error_info = {
            "block_type": None
        }
        # IF DO BLOCKS
        if_do_blocks = root.findall('.//ns:block[@type="controls_if"]', ns)
        for block in if_do_blocks:
            # Find all the blocks inside the if else block
            values = block.findall('.//ns:value', ns)
            # The first value should be the if else conditional. If it is not, it means the block is incomplete.
            if len(values) == 0:
                error_info["block_type"] = "controls_if"
            if values[0].get("name") == "IF0":
                pass
            else:
                error_info["block_type"] = "controls_if"
        # IF DO ELSE DO BLOCKS
        if_do_else_do_blocks = root.findall('.//ns:block[@type="controls_ifelse"]', ns)
        for block in if_do_else_do_blocks:
            # Find all the blocks inside the if else block
            values = block.findall('.//ns/value', ns)
            # The first value should be the if else conditional. If it is not, it means the block is incomplete.
            if len(values) == 0:
                error_info["block_type"] = "controls_ifelse"
            if values[0].get("name") == "IF0":
                pass
            else:
                error_info["block_type"] = "controls_ifelse"
        return error_info

    @staticmethod
    def generate_transformation_hint() -> str:
        """Generate a transformation hint based on the error."""
        return "To fix this issue, you need to ensure that the block is complete by filling all empty fields.\n"

    @staticmethod
    def generate_behavior_hint() -> str:
        """Generate a behavior hint based on the error."""
        return ("Incomplete block sequences can cause your code to behave unexpectedly. Not filling in all empty "
                "fields makes a block incomplete. If do blocks should do an action based on a condition. If do else "
                "do blocks should do an action based on a condition and another action if the condition is false.\n")

    @staticmethod
    def generate_location_hint(error_info: dict) -> str:
        """Generate a location hint based on the error."""
        block_mapping = {
            "controls_if": "if do",
            "controls_ifelse": "if do else do"
        }
        block = block_mapping[error_info["block_type"]] if error_info["block_type"] in block_mapping else None
        return (f"This issue was found in an \"{block}\" block. Check those blocks and find the one where the "
                f"if condition is missing.\n")

    @staticmethod
    def generate_example_hint() -> str:
        """Generate an example hint based on the error."""
        return ("For example, if you have an if do block, you should have a condition in the block to determine if "
                "the action should be executed or not. If you have an if do else do block, you should have a condition"
                "and an action to execute if the condition is false. This condition should be in the first field of "
                "the block and can be any logical comparison or boolean value.\n")
