"""Line (code) coverage tests for hotel_booking.py. SRN: PES1UG24AM085"""
import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---- booking_cost ----
def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


def test_zero_nights_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 1, False)


def test_peak_season_surcharge():
    # rate 3500 + 875 = 4375 for one night
    assert booking_cost("deluxe", 1, 2, True) == 4375


def test_extra_guests_charge():
    # 6000 + (3 - 2) * 500 * 1
    assert booking_cost("suite", 1, 3, False) == 6500


def test_long_stay_discount():
    # 2000 * 7 = 14000, minus 10%
    assert booking_cost("standard", 7, 2, False) == 12600


# ---- cancellation_refund ----
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_half_refund():
    assert cancellation_refund(1000, 3, False) == 500


def test_no_refund_last_minute():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_bonus_refund():
    assert cancellation_refund(1000, 3, True) == 750


# ---- room_upgrade ----
def test_no_rooms_free_no_upgrade():
    assert room_upgrade("standard", True, 0) == "standard"


def test_member_standard_to_deluxe():
    assert room_upgrade("standard", True, 5) == "deluxe"


def test_member_deluxe_to_suite():
    assert room_upgrade("deluxe", True, 5) == "suite"


def test_suite_stays_suite():
    assert room_upgrade("suite", True, 5) == "suite"
