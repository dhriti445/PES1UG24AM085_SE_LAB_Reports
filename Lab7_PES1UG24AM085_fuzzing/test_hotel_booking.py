import string

from hypothesis import assume, given, strategies as st

from hotel_booking import nights_stayed, room_floor, booking_label


# ---------- Fuzz tests: functions must never crash ----------
@given(st.text() | st.none())
def test_nights_stayed_no_crash(s):
    try:
        nights_stayed(s)
    except Exception as e:
        assert False, f"nights_stayed crashed with: {e!r}"


@given(st.text() | st.none())
def test_room_floor_no_crash(s):
    try:
        room_floor(s)
    except Exception as e:
        assert False, f"room_floor crashed with: {e!r}"


@given(st.text() | st.none())
def test_booking_label_no_crash(s):
    try:
        booking_label(s)
    except Exception as e:
        assert False, f"booking_label crashed with: {e!r}"


# ---------- Extra fuzzing: non-string types ----------
@given(st.one_of(st.integers(), st.floats(), st.lists(st.integers()),
                 st.booleans(), st.binary()))
def test_all_functions_reject_non_strings(x):
    assert nights_stayed(x) is None
    assert room_floor(x) is None
    assert booking_label(x) is None


# ---------- Property tests: valid input gives correct output ----------
@given(st.integers(0, 10**6), st.integers(0, 10**6))
def test_nights_stayed_correct(a, b):
    assume(b >= a)
    assert nights_stayed(f"{a}-{b}") == b - a


@given(st.integers(0, 10**6), st.integers(0, 10**6))
def test_nights_stayed_checkout_before_checkin_is_invalid(a, b):
    assume(b < a)
    assert nights_stayed(f"{a}-{b}") is None


@given(st.sampled_from("ABCD"), st.integers(0, 9), st.integers(0, 99))
def test_room_floor_correct(letter, floor, rest):
    assert room_floor(f"{letter}-{floor}{rest:02d}") == floor


@given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1),
                min_size=1, max_size=5))
def test_booking_label_correct(names):
    lead = names[0]
    expected = lead[0].upper() + lead[1:] + f" +{len(names) - 1}"
    assert booking_label(", ".join(names)) == expected


# ---------- Explicit edge cases found by fuzzing ----------
def test_known_edge_cases():
    assert nights_stayed("12-15") == 3
    assert nights_stayed("") is None
    assert nights_stayed("1215") is None
    assert nights_stayed("1-2-3") is None
    assert nights_stayed("a-b") is None
    assert room_floor("D-305") == 3
    assert room_floor("D-") is None
    assert room_floor("D305") is None
    assert room_floor("D-abc") is None
    assert booking_label("ravi, priya") == "Ravi +1"
    assert booking_label("") is None
    assert booking_label(",a") == "A +0"
    assert booking_label(" , ") is None
