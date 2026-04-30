class VehicleRepository:
    def __init__(self):
        self._vehicles = {
            1: {"model": "Hatch", "available": True},
            2: {"model": "Sedan", "available": True},
            3: {"model": "SUV", "available": False},
        }

    def exists(self, vehicle_id: int) -> bool:
        return vehicle_id in self._vehicles

    def is_available(self, vehicle_id: int) -> bool:
        if vehicle_id not in self._vehicles:
            return False
        return self._vehicles[vehicle_id]["available"]

    def mark_unavailable(self, vehicle_id: int) -> None:
        if vehicle_id not in self._vehicles:
            raise ValueError("Vehicle not found")
        self._vehicles[vehicle_id]["available"] = False

    def mark_available(self, vehicle_id: int) -> None:
        if vehicle_id not in self._vehicles:
            raise ValueError("Vehicle not found")
        self._vehicles[vehicle_id]["available"] = True
