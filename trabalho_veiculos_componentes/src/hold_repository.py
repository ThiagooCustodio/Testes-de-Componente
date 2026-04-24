class HoldRepository:
    def __init__(self):
        self._holds = []

    def add_hold(self, driver_id: int, vehicle_id: int) -> None:
        self._holds.append({"driver_id": driver_id, "vehicle_id": vehicle_id})

    def has_hold(self, driver_id: int, vehicle_id: int) -> bool:
        return any(
            entry["driver_id"] == driver_id and entry["vehicle_id"] == vehicle_id
            for entry in self._holds
        )

    def has_any_hold(self, vehicle_id: int) -> bool:
        return any(entry["vehicle_id"] == vehicle_id for entry in self._holds)

    def next_driver(self, vehicle_id: int):
        for entry in self._holds:
            if entry["vehicle_id"] == vehicle_id:
                return entry["driver_id"]
        return None

    def remove_hold(self, driver_id: int, vehicle_id: int) -> None:
        for entry in list(self._holds):
            if entry["driver_id"] == driver_id and entry["vehicle_id"] == vehicle_id:
                self._holds.remove(entry)
                return
        raise ValueError("Hold entry not found")
