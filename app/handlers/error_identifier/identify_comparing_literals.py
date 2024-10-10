"""This module contains functions to identify comparing literals."""
import xml.etree.ElementTree as ET


def check_comparing_literals_error(code: str) -> bool:
    """Returns True if there is a possible error related to comparing literals."""
    root = ET.fromstring(code)
    ns = {'ns': 'http://www.w3.org/1999/xhtml'}
    # Find all the blocks that compare 2 objects
    logic_compare_blocks = root.findall('.//ns:block[@type="logic_compare"]', ns)
    for block in logic_compare_blocks:
        # Comparison values
        value_a_block = block.find('.//ns:value[@name="A"]/ns:block', ns)
        value_b_block = block.find('.//ns:value[@name="B"]/ns:block', ns)

        # Comparing 2 string values
        if value_a_block.get("type") == "text" and value_b_block.get("type") == "text":
            return True
        # Comparing 2 number values
        elif value_a_block.get("type") == "math_number" and value_b_block.get("type") == "math_number":
            return True
        # Comparing 2 boolean values
        elif value_a_block.get("type") == "logic_boolean" and value_b_block.get("type") == "logic_boolean":
            return True

    return False
