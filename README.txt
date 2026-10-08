SOFTWARE QUALITY ENGINEERING - ASSIGNMENT 2
Name: Hira Shahid
Roll Number: FA23-BSE-029

WHAT YOU HAVE TO DO
1. Design at least 15 tests from the specification.
2. Use Boundary Value Analysis, Equivalence Partitioning, and Decision Table/Pairwise testing.
3. Automate the design in tests/test_fines.py using pytest.
4. Use parameterization, a fixture, pytest.raises, and unittest.mock.patch.
5. Run the suite on the original defective fines.py and record the failures.
6. Correct fines.py.
7. Run the suite again and measure statement + branch coverage.
8. Reach at least 90% coverage and show --fail-under=90 returns exit code 0.
9. Submit the design PDF, tests, corrected fines.py, and screenshots in one ZIP.

COMMANDS
pytest
coverage erase
coverage run --branch -m pytest
coverage report --fail-under=90

FINAL RESULT
43 passed
100% statement coverage
100% branch coverage
--fail-under=90 exit code: 0
