"""Helper functions for the handlers module."""
import xml.etree.ElementTree as ET


def find_parent_with_type(root, child):
    """Find the parent of a child element with a 'type' attribute."""
    for elem in root.iter():
        for subelem in elem:
            if subelem == child:
                # If this element has a 'type' attribute, return it
                if 'type' in elem.attrib:
                    return elem
                else:
                    # Recursively search up the tree
                    return find_parent_with_type(root, elem)
    return None


def check_variable_type(variable_name: str, root: ET, ns: dict) -> str:
    """Returns the type of the variable."""
    variable_blocks = root.findall('.//ns:block[@type="variables_set"]', ns)
    for block in variable_blocks:
        # Check if this `variables_set` block is setting the specified variable
        var_field = block.find(".//ns:field[@name='VAR']", ns)
        if var_field is not None and var_field.text == variable_name:
            # Check the type of the assigned value block
            value_block = block.find(".//ns:value/ns:block", ns)
            if value_block is not None:
                block_type = value_block.get("type")
                return block_type

    return "none_type"
