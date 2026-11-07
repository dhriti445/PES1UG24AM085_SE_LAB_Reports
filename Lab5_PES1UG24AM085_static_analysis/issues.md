# Lab 5 – Issues Table (radio_schedule.py)
**SRN:** PES1UG24AM085

Line numbers refer to the original file (`commits/00_original.py`).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection via string formatting (Bandit B608) – **Medium** | Security | 12 | `INSERT` built with `%` formatting, so a show name like `x'); DROP TABLE slots;--` alters the query | Parameterised query with `?` placeholders and a values tuple |
| Use of `eval()` (Bandit B307) – **Medium** | Security | 22 | `overlapFree` evaluates an arbitrary string, allowing code execution | Removed `eval`; `overlap_free(start, duration, next_start)` does the arithmetic directly |
| Hardcoded password (Bandit B105) – **Low** | Security | 6 | `STUDIO_PASSWORD = "onair2024"` is committed in source | Read from the `STUDIO_PASSWORD` environment variable |
| Broad exception `except Exception` (Pylint W0718) | Bug / Quality | 23 | Swallows every error and returns `False`, hiding real bugs | Removed with `eval`; no try/except needed |
| Global state / `global` statement (Pylint W0603) | Design | 7, 11 | `booked_minutes` global is never decremented on `removeSlot`, so it goes stale | Removed global; `booked_minutes()` computes `SUM(minutes)` from the DB; wrapped state in `RadioSchedule` class |
| Logic bug in `morningShows` | Bug | 28 | Guard `booked_minutes > 0` depends on the stale global, so morning shows can be wrongly hidden | Guard removed; query runs directly |
| Missing docstrings (C0114/C0115/C0116) | Style | 1, all defs | No module, class or function docstrings | Added docstrings |
| Function names not snake_case (C0103) | Style | 10, 16, 20, 27, 32 | `addSlot`, `slotLabel`, etc. violate PEP 8 | Renamed to `add_slot`, `slot_label`, `overlap_free`, `morning_shows`, `remove_slot` |
| Statement on same line as `if` (Flake8 E701) | Style | 28 | `if ...: return ...` on one line | Split onto separate lines |
| Line too long (Flake8 E501) | Style | 4, 12, 28 | Lines exceed 79 characters | Wrapped strings and arguments |
| Missing blank lines before `main()` call (Flake8 E305) | Style | 43 | Needs two blank lines after function | Added blank lines |
| Outdated `.format()` (Pylint C0209) | Style | 17 | `consider-using-f-string` | Switched to an f-string |
| `main()` runs on import | Design | 43 | No `__main__` guard | Added `if __name__ == "__main__":` |

## Commit mapping
1. Bandit fixes → `commits/01_bandit.py`
2. Flake8 fixes → `commits/02_flake8.py`
3. Pylint fixes → `radio_schedule.py`
