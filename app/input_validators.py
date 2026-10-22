"""Input validation for the calculator."""

from app.exceptions import ValidationError


class InputValidator:
    """Validates and normalizes user-supplied numbers."""

    @staticmethod
    def validate_number(value, max_input_value: float = 1e15) -> float:
        """Validate that value is numeric and within allowed range."""
        try:
            number = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid number: {value}")

        if abs(number) > max_input_value:
            raise ValidationError(
                f"Value {number} exceeds maximum allowed input of {max_input_value}"
            )
        return number