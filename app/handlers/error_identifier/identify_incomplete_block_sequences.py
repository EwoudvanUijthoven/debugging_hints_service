"""This module contains functions to identify incomplete block sequences."""
import xml.etree.ElementTree as ET


def check_incomplete_block_sequences_error(code: str) -> bool:
    """Returns True if there is a possible error related to incomplete block sequences."""
    root = ET.fromstring(code)
    ns = {'ns': 'http://www.w3.org/1999/xhtml'}
    # IF DO BLOCKS
    if_do_blocks = root.findall('.//ns:block[@type="controls_if"]', ns)
    for block in if_do_blocks:
        # Find all the blocks inside the if else block
        values = block.findall('.//ns:value', ns)
        # The first value should be the if else conditional. If it is not, it means the block is incomplete.
        if len(values) == 0:
            return True
        if values[0].get("name") == "IF0":
            pass
        else:
            return True
    # IF DO ELSE DO BLOCKS
    if_do_else_do_blocks = root.findall('.//ns:block[@type="controls_ifelse"]', ns)
    for block in if_do_else_do_blocks:
        # Find all the blocks inside the if else block
        values = block.findall('.//ns/value', ns)
        # The first value should be the if else conditional. If it is not, it means the block is incomplete.
        if len(values) == 0:
            return True
        if values[0].get("name") == "IF0":
            pass
        else:
            return True

    return False
