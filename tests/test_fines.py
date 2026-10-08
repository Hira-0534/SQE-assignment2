# Name: Hira Shahid
# Roll Number: FA23-BSE-029
# Software Quality Engineering - Assignment 2

from unittest.mock import patch
import pytest

from fines import calculate_fine, send_overdue_notice


@pytest.fixture
def member_email():
    return "student@example.com"


# Target: TC-01, TC-02, TC-03
@pytest.mark.parametrize("days, member, item, expected", [
    (10, "student", "book", 4.00),
    (5, "guest", "media", 6.00),
    (6, "staff", "reserve", 4.00),
])
def test_normal_fine_calculations(days, member, item, expected):
    assert calculate_fine(days, member, item) == expected


# Target: TC-04, TC-05, TC-06, TC-07
@pytest.mark.parametrize("days, expected", [
    (-1, 0.00),
    (0, 0.00),
    (2, 0.00),
    (3, 0.50),
])
def test_grace_period_boundaries(days, expected):
    assert calculate_fine(days, "student", "book") == expected


# Target: TC-08, TC-09, TC-10, TC-11, TC-12, TC-13, TC-14, TC-15, TC-16
@pytest.mark.parametrize("member, item, expected", [
    ("student", "book", 4.00),
    ("staff", "book", 2.00),
    ("guest", "book", 8.00),
    ("student", "media", 8.00),
    ("staff", "media", 4.00),
    ("guest", "media", 16.00),
    ("student", "reserve", 16.00),
    ("staff", "reserve", 8.00),
    ("guest", "reserve", 32.00),
])
def test_member_item_decision_combinations(member, item, expected):
    assert calculate_fine(10, member, item) == expected


# Target: TC-17, TC-18, TC-19, TC-20, TC-21
@pytest.mark.parametrize("member, item, expected", [
    ("student", "book", 50.00),
    ("staff", "book", 27.00),
    ("guest", "book", 50.00),
    ("student", "media", 50.00),
    ("guest", "media", 50.00),
])
def test_cap_is_applied_after_multiplier(member, item, expected):
    assert calculate_fine(110, member, item) == expected


# Target: TC-22, TC-23, TC-24
@pytest.mark.parametrize("member, expected", [
    ("student", 216.00),
    ("staff", 108.00),
    ("guest", 432.00),
])
def test_reserve_has_no_cap(member, expected):
    assert calculate_fine(110, member, "reserve") == expected


# Target: TC-25, TC-26, TC-27
@pytest.mark.parametrize("value", ["5", 2.5, None])
def test_non_integer_days_raise_type_error(value):
    with pytest.raises(TypeError) as exc:
        calculate_fine(value, "student", "book")
    assert str(exc.value) == "days_overdue must be an int"


# Target: TC-28, TC-29, TC-30, TC-31
@pytest.mark.parametrize("member", ["alumni", "admin", "", None])
def test_invalid_member_type_raises_value_error(member):
    with pytest.raises(ValueError):
        calculate_fine(5, member, "book")


# Target: TC-32, TC-33, TC-34, TC-35
@pytest.mark.parametrize("item", ["dvd", "magazine", "", None])
def test_invalid_item_type_raises_value_error(item):
    with pytest.raises(ValueError):
        calculate_fine(5, "student", item)


# Target: TC-36, TC-37, TC-38
@pytest.mark.parametrize("fine", [0.00, 4.99, 5.00])
def test_notice_not_sent_at_or_below_threshold(member_email, fine):
    with patch("fines._deliver_email") as mock_deliver:
        result = send_overdue_notice(member_email, fine)
    assert result == {"sent": False, "error": "Fine below notice threshold"}
    mock_deliver.assert_not_called()


# Target: TC-39, TC-40, TC-41
@pytest.mark.parametrize("fine", [5.01, 6.00, 50.00])
def test_notice_sent_above_threshold(member_email, fine):
    with patch("fines._deliver_email") as mock_deliver:
        result = send_overdue_notice(member_email, fine)
    assert result == {"sent": True, "error": None}
    mock_deliver.assert_called_once_with(member_email, fine)


# Target: TC-42
def test_notice_connection_error_is_handled(member_email):
    with patch("fines._deliver_email", side_effect=ConnectionError("server unavailable")):
        result = send_overdue_notice(member_email, 6.00)
    assert result == {"sent": False, "error": "SMTP error: server unavailable"}


# Target: TC-43
def test_deliver_email_builds_and_sends_message(member_email):
    class FakeSMTP:
        def __init__(self, host, port, timeout):
            self.host = host
            self.port = port
            self.timeout = timeout
            self.message = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def send_message(self, message):
            self.message = message

    fake = FakeSMTP("smtp.must.edu.pk", 25, 5)
    with patch("fines.smtplib.SMTP", return_value=fake):
        from fines import _deliver_email
        _deliver_email(member_email, 6.25)
    assert fake.message["To"] == member_email
    assert fake.message["Subject"] == "Overdue library item"
