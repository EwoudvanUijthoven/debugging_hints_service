"""Identifies an error based on either the error message or the code."""


def identify_error_handler(error_message: str, code: str) -> str:
    """Function to identify which error and return a unique error name."""
    if "ZeroDivisionError" in error_message:
        return "zero_division_error"
    elif "IndexError" in error_message:
        return "out_of_bounds_error"
    elif "TypeError" in error_message:
        return "type_error"
    elif "AttributeError: 'NoneType' object has no attribute" in error_message:
        return "none_type_error"
    elif check_comparing_literals_error(code):
        return "comparing_literals_error"
    else:
        raise NotImplementedError("No handled error found! Error message: " + error_message)
