class RentalService:
    def __init__(self, vehicle_repository, driver_repository, rental_repository, hold_repository):
        self.vehicle_repository = vehicle_repository
        self.driver_repository = driver_repository
        self.rental_repository = rental_repository
        self.hold_repository = hold_repository

    def rent_vehicle(self, driver_id: int, vehicle_id: int) -> bool:
        if not driver_id or not vehicle_id:
            raise ValueError("Driver ID and vehicle ID are required")

        if not self.driver_repository.exists(driver_id):
            return False

        if not self.vehicle_repository.exists(vehicle_id):
            return False

        if self.driver_repository.is_blocked(driver_id):
            return False

        if not self.driver_repository.has_valid_license(driver_id):
            return False

        if not self.vehicle_repository.is_available(vehicle_id):
            # só bloqueia se NÃO for o motorista da reserva
            if not self.hold_repository.has_hold(driver_id, vehicle_id):
                return False

        if self.rental_repository.count_active_rentals(driver_id) >= 2:
            return False

        next_driver = self.hold_repository.next_driver(vehicle_id)
        if next_driver is not None and next_driver != driver_id:
            return False

        self.vehicle_repository.mark_unavailable(vehicle_id)
        self.rental_repository.create_rental(driver_id, vehicle_id)

        if self.hold_repository.has_hold(driver_id, vehicle_id):
            self.hold_repository.remove_hold(driver_id, vehicle_id)

        return True

    def return_vehicle(self, driver_id: int, vehicle_id: int) -> bool:
        if not driver_id or not vehicle_id:
            raise ValueError("Driver ID and vehicle ID are required")

        if not self.rental_repository.is_vehicle_with_driver(driver_id, vehicle_id):
            return False

        self.rental_repository.close_rental(driver_id, vehicle_id)

        if not self.hold_repository.has_any_hold(vehicle_id):
            self.vehicle_repository.mark_available(vehicle_id)

        return True

    def hold_vehicle(self, driver_id: int, vehicle_id: int) -> bool:
        if not driver_id or not vehicle_id:
            raise ValueError("Driver ID and vehicle ID are required")

        if not self.driver_repository.exists(driver_id):
            return False

        if not self.vehicle_repository.exists(vehicle_id):
            return False

        if self.driver_repository.is_blocked(driver_id):
            return False

        if not self.driver_repository.has_valid_license(driver_id):
            return False

        if self.vehicle_repository.is_available(vehicle_id):
            return False

        if self.hold_repository.has_hold(driver_id, vehicle_id):
            return False

        if self.rental_repository.is_vehicle_with_driver(driver_id, vehicle_id):
            return False

        self.hold_repository.add_hold(driver_id, vehicle_id)
        return True
