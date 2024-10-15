"""Helper functions for the handlers module."""


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