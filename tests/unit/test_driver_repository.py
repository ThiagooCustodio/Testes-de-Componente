from src.driver_repository import DriverRepository


def test_exists_returns_true_for_known_driver():
    repo = DriverRepository()
    assert repo.exists(10) is True


def test_exists_returns_false_for_unknown_driver():
    repo = DriverRepository()
    assert repo.exists(999) is False


def test_is_blocked_returns_true_when_driver_is_blocked():
    repo = DriverRepository()
    assert repo.is_blocked(20) is True


def test_has_valid_license_returns_false_when_license_is_invalid():
    repo = DriverRepository()
    assert repo.has_valid_license(30) is False
