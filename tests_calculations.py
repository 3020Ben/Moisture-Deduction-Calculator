# tests_calculations.py
import pytest
from calculations import (
    deducted_weight,
    moisture_content_range
)

# ----- Tests for deducted_weight function -----
@pytest.mark.parametrize(
    "net_weight, moisture_content, allowable_moisture, expected",
    [
        (1000, 14.21, 12, {"deducted_weight": 25, "payment_weight": 975}),
        (1080, 9.99, 10, {"deducted_weight": 0, "payment_weight": 1080}),
        (750, 16.79, 14, {"deducted_weight": 24, "payment_weight": 726}),
        (1920, 14.20, 10, {"deducted_weight": 90, "payment_weight": 1830}),
    ]
)
def test_deducted_weight(net_weight, moisture_content, allowable_moisture, expected):
    result = deducted_weight(net_weight, moisture_content, allowable_moisture)
    assert result == expected

# ----- Tests for moisture_content_range function -----
@pytest.mark.parametrize(
    "net_weight, desired_deduction, allowable_moisture, expected",
    [
        (1000, 25, 12, (14.16, 14.24)),
        (1080, 0, 10, (5.01, 9.99)),
        (750, 24, 14, (16.70, 16.80)),
        (1920, 90, 10, (14.20, 14.24)),
    ]
)
def test_moisture_content_range(net_weight, desired_deduction, allowable_moisture, expected):
    result = moisture_content_range(net_weight, desired_deduction, allowable_moisture)
    assert result == expected

