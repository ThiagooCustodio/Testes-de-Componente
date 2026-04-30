class DriverRepository:
    def __init__(self):
        self._drivers = {
            10: {"name": "Ana", "blocked": False, "valid_license": True},
            20: {"name": "Bruno", "blocked": True, "valid_license": True},
            30: {"name": "Carla", "blocked": False, "valid_license": False},
            40: {"name": "Diego", "blocked": False, "valid_license": True},
        }

    def exists(self, driver_id: int) -> bool:
        return driver_id in self._drivers

    def is_blocked(self, driver_id: int) -> bool:
        if driver_id not in self._drivers:
            return False
        return self._drivers[driver_id]["blocked"]

    def has_valid_license(self, driver_id: int) -> bool:
        if driver_id not in self._drivers:
            return False
        return self._drivers[driver_id]["valid_license"]
