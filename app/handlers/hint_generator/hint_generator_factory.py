"""Factory method to generate the class based on the error_name."""
from app.handlers.hint_generator.hint_generator_template import HintGenerator
from app.handlers.hint_generator.hint_generator_zero_division import ZeroDivisionHintGenerator
from app.handlers.hint_generator.hint_generator_comparing_literals import ComparingLiteralsHintGenerator


def hint_generator_factory(error_name: str, code: str, error: str) -> HintGenerator:
    """Factory method to generate the class based on the error_name."""
    if error_name == "zero_division_error":
        return ZeroDivisionHintGenerator(code=code, error=error)
    elif error_name == "comparing_literals_error":
        return ComparingLiteralsHintGenerator(code=code, error=error)
    # elif error_name == "out_of_bounds_error":
    #     return OutOfBoundsHintGenerator()
    else:
        raise NotImplementedError("No hint generator found for this error.")
