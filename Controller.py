from anki import Controller, TrackPiece, errors
from anki.control.vehicle import BatteryState
from typing import Collection, Optional
from anki.control.scanner import BaseScanner
import asyncio

from Vehicle import VehicleEmulation
from Scanner import DummyScanner


class ControllerEmulation(Controller):
    async def _get_vehicle(
        self,
        vehicle_id: Optional[int]=None,
        address: str|None=None
        ) -> VehicleEmulation:
        # Finds a Supercar and creates a Vehicle instance around it

        vehicle_ids = {v.id for v in self.vehicles}
        if vehicle_id is None:
            # Automatically assign generate unused vehicle id
            vehicle_id = 1024
            while vehicle_id in vehicle_ids:
                vehicle_id += 1
                pass
            pass
        elif vehicle_id in vehicle_ids:
            raise RuntimeError(f"Duplicate id for vehicle. Id {vehicle_id} already in use.")

        vehicle = VehicleEmulation(
            vehicle_id,
            None,
            None,
            self,
            battery = BatteryState(True,False,False,False)
        )
        self.vehicles.add(vehicle)
        return vehicle
