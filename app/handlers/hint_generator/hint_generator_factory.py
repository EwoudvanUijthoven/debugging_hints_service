"""Factory method to generate the class based on the error_name."""
from app.handlers.hint_generator.hint_generator_template import HintGenerator
from app.handlers.hint_generator.hint_generator_zero_division import ZeroDivisionHintGenerator
from app.handlers.hint_generator.hint_generator_comparing_literals import ComparingLiteralsHintGenerator
from app.handlers.hint_generator.hint_generator_out_of_bounds import OutOfBoundsHintGenerator
from app.handlers.hint_generator.hint_generator_type_error import TypeErrorHintGenerator
from app.handlers.hint_generator.hint_generator_ambiguous_parameter_name import AmbiguousParameterNameHintGenerator
from app.handlers.hint_generator.hint_generator_incomplete_block_sequences import IncompleteBlockSequencesGenerator
from app.handlers.hint_generator.hint_generator_parameter_out_of_scope import ParameterOutOfScopeHintGenerator


def hint_generator_factory(error_name: str, code: str, error: str) -> HintGenerator:
    """Factory method to generate the class based on the error_name."""
    if error_name == "zero_division_error":
        return ZeroDivisionHintGenerator(code=code, error=error)
    elif error_name == "comparing_literals_error":
        return ComparingLiteralsHintGenerator(code=code, error=error)
    elif error_name == "out_of_bounds_error":
        return OutOfBoundsHintGenerator(code=code, error=error)
    elif error_name == "type_error":
        return TypeErrorHintGenerator(code=code, error=error)
    elif error_name == "ambiguous_parameter_name":
        return AmbiguousParameterNameHintGenerator(code=code, error=error)
    elif error_name == "incomplete_block_sequences_error":
        return IncompleteBlockSequencesGenerator(code=code, error=error)
    elif error_name == "parameter_out_of_scope_error":
        return ParameterOutOfScopeHintGenerator(code=code, error=error)
    else:
        raise NotImplementedError("No hint generator found for this error.")
