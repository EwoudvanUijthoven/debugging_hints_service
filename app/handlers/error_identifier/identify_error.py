"""Identifies an error based on either the error message or the code."""
from app.handlers.error_identifier.identify_comparing_literals import check_comparing_literals_error
from app.handlers.error_identifier.identify_incomplete_block_sequences import check_incomplete_block_sequences_error
from app.handlers.error_identifier.identify_parameter_out_of_scope import check_parameter_out_of_scope_error
from typing import Union


def identify_error_handler(error_message: str, code: str, output: str, status: str, code_language: str) -> str:
    """Function to identify which error and return a unique error name."""
    if code_language == "Python":
        # If the status is 1, it means the program run unsuccessfully, and we have a real error.
        if status == "1":
            return identify_real_python_error_handler(error_message=error_message)
        # If the status is 0, it means the program run successfully, there might be an error that is silently skipped.
        elif status == "0":
            return identify_silent_error_handler(code=code)
        # Other status codes should not appear and are not supported.
        else:
            raise NotImplementedError(f"This error status is not supported: {status}")
    elif code_language == "Arduino":
        # Arduino should output 0 as the upload should always have worked at this point.
        if status == "0":
            real_error = identify_real_arduino_error_handler(error_message=error_message)
            if real_error:
                return real_error
            else:
                return identify_silent_error_handler(code=code)
        # Other status codes should not appear and are not supported.
        else:
            raise NotImplementedError(f"This error status is not supported: {status}")


def identify_real_python_error_handler(error_message: str) -> str:
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


def identify_real_arduino_error_handler(error_message: str) -> Union[str, None]:
    """Function to identify which error and return a unique error name."""
    if "warning: division by zero" in error_message:
        return "zero_division_error"
    elif "error: index out of bounds for" in error_message:
        return "out_of_bounds_error"
    elif "error: no match for" in error_message:
        return "type_error"
    elif "error: redefinition of" in error_message:
        return "ambiguous_parameter_name"
    elif "was not declared in this scope" in error_message:
        return "none_type_error"
    else:
        return None


def identify_silent_error_handler(code: str) -> str:
    """Function to identify which error and return a unique error name."""
    if check_comparing_literals_error(code):
        return "comparing_literals_error"
    elif check_incomplete_block_sequences_error(code):
        return "incomplete_block_sequences_error"
    elif check_parameter_out_of_scope_error(code):
        return "parameter_out_of_scope_error"
    else:
        raise NotImplementedError("No handled silent error could be found!")
