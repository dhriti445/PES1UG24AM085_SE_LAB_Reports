# Lab 5 – Reflection
**SRN:** PES1UG24AM085

**1. Which issues were the easiest to fix, and which were the hardest? Why?**
Easiest were the Flake8 formatting issues (E302, E305, E501, E701) and missing docstrings: the message points to the exact line and the fix is mechanical. Hardest was the `eval()` and global-state combination. Removing `eval` meant redesigning `overlapFree` to take numbers, and fixing the stale `booked_minutes` global meant restructuring the module into a class so state is computed from the database.

**2. Did the tools report any false positives?**
Bandit's hardcoded-password warning (B105) is a low-severity heuristic: it flags the variable name, not proof of a real secret, and it was unused in the program. Treating it as a real issue was still sensible. Bandit does not flag the logic bug in `morningShows`; only reading the code (and Pylint's global warning hinting at it) revealed that, so tools complement, not replace, review.

**3. How would you integrate these tools into a real workflow?**
Run Flake8 and Pylint as pre-commit hooks, and run Bandit plus Pylint (with a minimum score threshold) in a CI pipeline such as GitHub Actions on every pull request, blocking merges on high/medium findings. Configure rules in `setup.cfg`/`.pylintrc` so the team agrees on what counts as a failure.

**4. What tangible improvements did you observe after the fixes?**
Security improved (no SQL injection, no `eval`, no hardcoded secret). Robustness improved because booked minutes is now always consistent with stored slots and the morning-shows bug is gone. Readability improved through snake_case names, docstrings, f-strings and a class that groups state with behaviour, and the module can now be imported without side effects.
