# validators.py
def validate_positive_int(value, name: str) -> int:
    """Validate that the given value is a positive integer.

    Args:
        value: The value to validate.
        name: The name of the parameter (used in error messages).
    
    Returns:
        int: The validated positive integer.
    
    Raises:
        ValueError: If the value is not a positive integer."""
    if not isinstance(value, int):
        raise ValueError(f"{name} must be an integer. Got:{value}")
    
    if value <= 0:
        raise ValueError(f"{name} must be a positive number. Got:{value}")
    
    return value


def validate_positive_number(value, name: str) -> float:
    """Validate that the given value is a positive number (int or float).
    Args:
        value: The value to validate.
        name: The name of the parameter (used in error messages).
    Returns:
        float: The validated positive number.
    Raises:
        ValueError: If the value is not a positive number."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number. Got:{value}")
    
    if value <= 0:
        raise ValueError(f"{name} must be a positive number. Got:{value}")
    
    return float(value)


def validate_allowable(value, allowable_values=[10, 12, 14], name="Allowable Moisture Content"):
    """Validate that the given value is in the allowable values.

    Args:
        value: The value to validate.
        allowable_values: A list of allowable values.
        name: The name of the parameter (used in error messages).
    Returns:
        The validated value.
    Raises:
        ValueError: If the value is not within the allowable values."""
    if value not in allowable_values:
        raise ValueError(f"{name} must be one of {allowable_values}. Got:{value}")
    
    return value
