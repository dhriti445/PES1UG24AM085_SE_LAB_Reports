"""Hotel booking helpers, hardened against invalid input (Lab 7).

Each function returns None when its input is invalid instead of crashing.
SRN: PES1UG24AM085
"""


def nights_stayed(days):
    """Return nights between 'check_in-check_out' (e.g. '12-15' -> 3).

    Returns None for non-strings, wrong format, non-numeric days, or a
    check-out earlier than check-in.
    """
    if not isinstance(days, str):
        return None
    parts = days.split('-')
    if len(parts) != 2:
        return None
    try:
        check_in = int(parts[0].strip())
        check_out = int(parts[1].strip())
    except ValueError:
        return None
    if check_out < check_in:
        return None
    return check_out - check_in


def room_floor(room_code):
    """Return the floor from a code like 'D-305' (-> 3), else None."""
    if not isinstance(room_code, str):
        return None
    parts = room_code.split('-')
    if len(parts) != 2:
        return None
    number = parts[1].strip()
    if not number:
        return None
    try:
        return int(number[0])
    except ValueError:
        return None


def booking_label(names_csv):
    """Return 'Lead +N' for a CSV of guest names, else None."""
    if not isinstance(names_csv, str):
        return None
    names = [n.strip() for n in names_csv.split(',') if n.strip()]
    if not names:
        return None
    lead = names[0]
    return lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)


def main():
    """Interactive demo."""
    print("==== Running nights_stayed ====")
    user_input = input("Enter check-in and check-out day (e.g. 12-15): ")
    result = nights_stayed(user_input)
    print("Nights:", "Invalid input" if result is None else result)

    print("\n==== Running room_floor ====")
    user_input = input("Enter a room code (e.g. D-305): ")
    result = room_floor(user_input)
    print("Floor:", "Invalid input" if result is None else result)

    print("\n==== Running booking_label ====")
    user_input = input("Enter guest names as CSV (e.g. ravi, priya): ")
    result = booking_label(user_input)
    print("Booking Label:", "Invalid input" if result is None else result)


if __name__ == "__main__":
    main()
