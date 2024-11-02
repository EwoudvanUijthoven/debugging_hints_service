"""This module contains functions to identify type error."""
import xml.etree.ElementTree as ET
from app.handlers.utils.helper_functions import check_variable_type


def check_type_error(code: str) -> bool:
    """Returns True if there is a possible error related to types."""
    root = ET.fromstring(code)
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
            return True

    return False
