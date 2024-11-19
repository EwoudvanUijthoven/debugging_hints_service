"""Identifies an error based on either the error message or the code."""
from app.handlers.error_identifier.identify_comparing_literals import check_comparing_literals_error
from app.handlers.error_identifier.identify_incomplete_block_sequences import check_incomplete_block_sequences_error
from app.handlers.error_identifier.identify_parameter_out_of_scope import check_parameter_out_of_scope_error


def identify_error_handler(error_message: str, code: str, output: str, status: str) -> str:
    """Function to identify which error and return a unique error name."""
    # If the status is 1, it means the program run unsuccessfully, and we have a real error.
    if status == "1":
        return identify_real_error_handler(error_message, code, output, status)
    # If the status is 0, it means the program run successfully, there might be an error that is silently skipped.
    elif status == "0":
        return identify_silent_error_handler(error_message, code, output, status)
    # Other status codes should not appear and are not supported.
    else:
        raise NotImplementedError(f"This error status is not supported: {status}")


def identify_real_error_handler(error_message: str, code: str, output: str, status: str) -> str:
    """Function to identify which error and return a unique error name."""
    if "ZeroDivisionError" in error_message:
        return "zero_division_error"
    elif "IndexError" in error_message:
        return "out_of_bounds_error"
    elif "TypeError" in error_message:
        return "type_error"
    elif "SyntaxError: duplicate argument 'x' in function definition" in error_message:
        return "ambiguous_parameter_name"
    elif "AttributeError: 'NoneType' object has no attribute" in error_message:
        return "none_type_error"
    else:
        raise NotImplementedError(f"An unhandled error found! Error message: {error_message}")


def identify_silent_error_handler(error_message: str, code: str, output: str, status: str) -> str:
    """Function to identify which error and return a unique error name."""
    if check_comparing_literals_error(code):
        return "comparing_literals_error"
    elif check_incomplete_block_sequences_error(code):
        return "incomplete_block_sequences_error"
    elif check_parameter_out_of_scope_error(code):
        return "parameter_out_of_scope_error"
    else:
        raise NotImplementedError("No handled silent error could be found!")
