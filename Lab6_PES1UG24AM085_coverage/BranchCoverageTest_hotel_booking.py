"""Branch coverage tests for hotel_booking.py. SRN: PES1UG24AM085

Covers every decision both True and False, including boundaries
(nights 1/6/7, guests 2/3, days_before 1/2/6/7, rooms_free 0/1).
"""
import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---- booking_cost: validation ----
def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


def test_zero_nights_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 1, False)


def test_negative_nights_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("deluxe", -3, 1, False)


# ---- booking_cost: is_peak_season True / False ----
def test_off_peak_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_peak_season_surcharge():
    assert booking_cost("deluxe", 1, 2, True) == 4375


# ---- booking_cost: guests > 2 True / False ----
def test_exactly_two_guests_no_extra():
    assert booking_cost("suite", 1, 2, False) == 6000


def test_three_guests_extra_charge():
    assert booking_cost("suite", 1, 3, False) == 6500


def test_extra_guests_multiply_by_nights():
    # 4000 + (4 - 2) * 500 * 2
    assert booking_cost("standard", 2, 4, False) == 6000


# ---- booking_cost: nights >= 7 True / False ----
def test_six_nights_no_discount():
    assert booking_cost("standard", 6, 2, False) == 12000


def test_seven_nights_discount():
    assert booking_cost("standard", 7, 2, False) == 12600


def test_all_modifiers_together():
    # rate 2500 * 7 = 17500, + 1 * 500 * 7 = 21000, - 10% = 18900
    assert booking_cost("standard", 7, 3, True) == 18900


# ---- cancellation_refund: days_before >= 7 / >= 2 / else ----
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_full_refund_boundary_seven_days():
    assert cancellation_refund(1000, 7, False) == 1000


def test_member_full_refund_no_bonus():
    assert cancellation_refund(1000, 10, True) == 1000


def test_half_refund_boundary_six_days():
    assert cancellation_refund(1000, 6, False) == 500


def test_half_refund_boundary_two_days():
    assert cancellation_refund(1000, 2, False) == 500


def test_no_refund_one_day():
    assert cancellation_refund(1000, 1, False) == 0


# ---- cancellation_refund: is_member True / False ----
def test_member_bonus_on_half_refund():
    assert cancellation_refund(1000, 3, True) == 750


def test_member_bonus_on_zero_refund():
    assert cancellation_refund(1000, 0, True) == 250


# ---- room_upgrade ----
def test_no_rooms_free_no_upgrade():
    assert room_upgrade("standard", True, 0) == "standard"


def test_member_standard_to_deluxe():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_non_member_standard_stays():
    assert room_upgrade("standard", False, 5) == "standard"


def test_member_deluxe_to_suite():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_non_member_deluxe_stays():
    assert room_upgrade("deluxe", False, 5) == "deluxe"


def test_member_suite_stays_suite():
    assert room_upgrade("suite", True, 5) == "suite"
