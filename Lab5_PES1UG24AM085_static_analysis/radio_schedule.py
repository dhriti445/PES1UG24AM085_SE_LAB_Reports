"""Radio station programme schedule.

Books show slots, lists morning shows, checks timing and removes slots.
Author SRN: PES1UG24AM085
"""

import os
import sqlite3

# Read from the environment instead of hardcoding a secret in source code.
STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD", "")


class RadioSchedule:
    """In-memory programme schedule backed by SQLite."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(
            "CREATE TABLE slots (id INTEGER PRIMARY KEY, show TEXT, "
            "host TEXT, start_hour INTEGER, minutes INTEGER)"
        )

    def add_slot(self, show, host, start_hour, minutes):
        """Book a show slot (parameterised query, no string formatting)."""
        self.conn.execute(
            "INSERT INTO slots (show, host, start_hour, minutes) "
            "VALUES (?, ?, ?, ?)",
            (show, host, start_hour, minutes),
        )

    def booked_minutes(self):
        """Return total booked minutes, always in sync with stored slots."""
        row = self.conn.execute(
            "SELECT COALESCE(SUM(minutes), 0) FROM slots"
        ).fetchone()
        return row[0]

    def morning_shows(self):
        """Return the names of shows starting before noon."""
        rows = self.conn.execute(
            "SELECT show FROM slots WHERE start_hour < 12"
        )
        return [row[0] for row in rows]

    def remove_slot(self, slot_id):
        """Delete the slot with the given id."""
        self.conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def slot_label(show, host):
    """Return a display label for a slot."""
    return f"{show} hosted by {host}"


def overlap_free(start_hour, duration_hours, next_start):
    """Return True if a slot ends before the next one starts."""
    return start_hour + duration_hours <= next_start


def main():
    """Run a short demonstration."""
    schedule = RadioSchedule()
    schedule.add_slot("Sunrise Beats", "Vik", 7, 60)
    schedule.add_slot("Midday Talk", "Anu", 13, 45)
    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free(7, 1, 13), schedule.morning_shows())
    schedule.remove_slot(2)
    print("Booked minutes:", schedule.booked_minutes())


if __name__ == "__main__":
    main()
