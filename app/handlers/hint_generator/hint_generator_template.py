"""Class to define a structure for a hint generator."""


class HintGenerator:
    """Class to define a structure for a hint generator."""

    def __init__(self, code: str, error: str):
        """Initialize the hint generator."""
        self.code = code
        self.error = error

    def generate_hint(self) -> str:
        """Generate a hint based on the error."""
        raise NotImplementedError("This method should be implemented in the child classes.")
