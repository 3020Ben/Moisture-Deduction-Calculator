# calculations.py
from validators import (validate_positive_int,
                         validate_positive_number,
                         validate_allowable)

# ----- Deduction calculator -----
def deducted_weight(net_weight: int, moisture_content: float, allowable_moisture: int) -> dict:
    """Calculate the deducted weight based on moisture content and allowable moisture.

    Args:
        net_weight: The net weight of the product.
        moisture_content: The actual moisture content percentage.
        allowable_moisture: The allowable moisture content percentage.
    Returns:
        dict: A dictionary containing 'deducted_weight' and 'payment_weight'. """
    validate_positive_int(net_weight, "Net Weight")
    validate_positive_number(moisture_content, "Moisture Content")
    validate_allowable(allowable_moisture, name="Allowable Moisture Content")

    if moisture_content <= allowable_moisture:
        return {
            "deducted_weight": 0,
            "payment_weight": net_weight
        }
    
    deduction = int(round(
        ((moisture_content - allowable_moisture) * net_weight) / (100 - allowable_moisture),
        0
        ))

    payment_weight = int(round(net_weight - deduction, 0))

    return {
        "deducted_weight": deduction,
        "payment_weight": payment_weight
    }


# ----- Moisture content calculator -----
def moisture_content_range(net_weight: int, desired_deduction: int, allowable_moisture: int) -> float:
    """Calculate the range of moisture content based on desired deduction and allowable moisture.

    Args:
        net_weight: The net weight of the delivery.
        desired_deduction: The desired weight to deduct from the net weight.
        allowable_moisture: The allowable moisture content percentage.
    Returns:
        int: The minimum moisture and maximum moisture."""
    validate_positive_int(net_weight, "Net Weight")
    validate_positive_int(desired_deduction, "Desired Deduction")
    validate_allowable(allowable_moisture, name="Allowable Moisture Content")

    # Compute base moisture
    base_moisture = round(
        ((desired_deduction * (100 - allowable_moisture)) / net_weight) + allowable_moisture,
        2
        )

    # ----- Find min moisture content -----
    m = base_moisture
    
    while True:
        result = deducted_weight(net_weight, m, allowable_moisture)

        if result["deducted_weight"] != desired_deduction:
            break

        m = round(m - 0.01, 2)
        if m <= 5.0: # Min moisture content limit
            break

    min_moisture = round(m + 0.01, 2)

    # ----- Find max moisture content -----
    m = base_moisture
    while True:
        result = deducted_weight(net_weight, m, allowable_moisture)

        if result["deducted_weight"] != desired_deduction:
            break

        m = round(m + 0.01, 2)
        if m >= 59.9: # Max moisture content limit
            break
    max_moisture = round(m - 0.01, 2)

    return min_moisture, max_moisture

def payment_weight(net_weight: int, deduction: int) -> int:
   """Calculate the payment weight based on the net weight and deduction.

    Args:
        net_weight: The net weight of the delivery.
        deduction: The weight deducted from the net weight.
    Returns:
        int: The payment weight."""
   
   payment_weight = round(net_weight - deduction, 0)
   return payment_weight

