class RentalRepository:
    def __init__(self):
        self._active_rentals = []

    def create_rental(self, driver_id: int, vehicle_id: int) -> None:
        self._active_rentals.append({"driver_id": driver_id, "vehicle_id": vehicle_id})

    def has_active_rental(self, vehicle_id: int) -> bool:
        return any(rental["vehicle_id"] == vehicle_id for rental in self._active_rentals)

    def is_vehicle_with_driver(self, driver_id: int, vehicle_id: int) -> bool:
        return any(
            rental["driver_id"] == driver_id and rental["vehicle_id"] == vehicle_id
            for rental in self._active_rentals
        )

    def count_active_rentals(self, driver_id: int) -> int:
        return sum(1 for rental in self._active_rentals if rental["driver_id"] == driver_id)

    def close_rental(self, driver_id: int, vehicle_id: int) -> None:
        for rental in list(self._active_rentals):
            if rental["driver_id"] == driver_id and rental["vehicle_id"] == vehicle_id:
                self._active_rentals.remove(rental)
                return
        raise ValueError("Active rental not found")
