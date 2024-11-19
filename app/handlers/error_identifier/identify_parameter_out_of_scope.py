"""This module contains functions to identify parameter out of scope."""
import xml.etree.ElementTree as ET


def check_parameter_out_of_scope_error(code: str) -> bool:
    """Returns True if there is a possible error related to parameter out of scope."""
    root = ET.fromstring(code)
    ns = {'ns': 'http://www.w3.org/1999/xhtml'}
    # Find all function definitions
    function_blocks_without_return = root.findall('.//ns:block[@type="procedures_defnoreturn"]', ns)
    function_blocks_with_return = root.findall('.//ns:block[@type="procedures_defreturn"]', ns)
    function_blocks = function_blocks_without_return + function_blocks_with_return
    for block in function_blocks:
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
                return True
    return False
