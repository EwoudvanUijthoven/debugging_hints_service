"""Generates hints for zero division errors."""
from app.handlers.hint_generator.hint_generator_template import HintGenerator


class ZeroDivisionHintGenerator(HintGenerator):
    """Generates hints for zero division errors."""

    def generate_hint(self) -> str:
        """Generate a hint based on the error."""
        return ("Hint: You encountered a ZeroDivisionError, which means you are attempting to divide a number by zero. "
                "This error typically occurs when the denominator in a division operation evaluates to zero. Check "
                "the variables or expressions being used as the denominator and add validation logic to ensure that "
                "the denominator is never zero before performing the division.")
